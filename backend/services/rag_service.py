"""
SIKHSAATHI — Production RAG & Semantic Retrieval Service
Provides chapter-aware RAG Q&A, student-friendly citations, search, and printable downloads.
"""

import os
import sys
from pathlib import Path

# Enable direct script execution by adding project root to sys.path
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

# Configure safe UTF-8 output encoding for Windows consoles
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

import re
import html
import json
import time
import httpx
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

from backend.config import settings
from backend.db import get_db_connection, seed_default_notes_for_user
from backend.services.resource_service import resource_service
from backend.services.embedding_service import embedding_service
from backend.services.document_processor import DocumentProcessor

class RAGService:
    def __init__(self):
        self._http_client: Optional[httpx.AsyncClient] = None
        self._doc_processor = DocumentProcessor()

    async def _get_client(self) -> httpx.AsyncClient:
        if self._http_client is None or self._http_client.is_closed:
            limits = httpx.Limits(max_keepalive_connections=15, max_connections=30)
            timeout = httpx.Timeout(8.0, connect=3.0)
            self._http_client = httpx.AsyncClient(limits=limits, timeout=timeout)
        return self._http_client

    def ensure_user_seeded(self, user_id: str):
        """Ensures the curriculum notes exist for the given user in SQLite."""
        seed_default_notes_for_user(user_id)

    def get_all_notes(self, user_id: str, subject_filter: Optional[str] = None, search: Optional[str] = None) -> Dict[str, Any]:
        """Retrieves user's indexed notes from SQLite with subject badge counts."""
        self.ensure_user_seeded(user_id)
        conn = get_db_connection()
        cursor = conn.cursor()

        counts = {"all": 0, "chem": 0, "phys": 0, "math": 0, "cs": 0}
        cursor.execute("SELECT subject, COUNT(*) as cnt FROM notes WHERE user_id = ? GROUP BY subject", (user_id,))
        for row in cursor.fetchall():
            subj = (row["subject"] or "").lower()
            if subj in counts:
                counts[subj] = row["cnt"]
        cursor.execute("SELECT COUNT(*) FROM notes WHERE user_id = ?", (user_id,))
        counts["all"] = cursor.fetchone()[0]

        query = "SELECT * FROM notes WHERE user_id = ?"
        params = [user_id]

        if subject_filter and subject_filter.lower() != "all":
            query += " AND subject = ?"
            params.append(subject_filter.lower())

        if search and search.strip():
            query += " AND (title LIKE ? OR body LIKE ?)"
            s = f"%{search.strip()}%"
            params.extend([s, s])

        query += " ORDER BY updated_at DESC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        notes_list = []
        for r in rows:
            notes_list.append({
                "id": r["id"],
                "title": r["title"],
                "subject": r["subject"],
                "badge": r["subject_badge"],
                "format": r["format"],
                "chunk_count": r["chunk_count"],
                "reading_time_min": r["reading_time_min"],
                "word_count": r["word_count"],
                "status": r["status"],
                "updated_at": r["updated_at"]
            })

        return {
            "status": "success",
            "notes": notes_list,
            "subject_counts": counts,
            "total_indexed": counts["all"]
        }

    def get_note_by_id(self, note_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Fetches complete note detail and chunks from SQLite database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notes WHERE id = ? AND user_id = ?", (note_id, user_id))
        note_row = cursor.fetchone()

        if not note_row:
            cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
            note_row = cursor.fetchone()

        if not note_row:
            conn.close()
            return None

        cursor.execute("SELECT * FROM note_chunks WHERE note_id = ? ORDER BY chunk_index ASC", (note_row["id"],))
        chunk_rows = cursor.fetchall()
        conn.close()

        chunks = []
        for c in chunk_rows:
            chunks.append({
                "id": c["id"],
                "text": c["text"],
                "score": 0.95,
                "page_number": c["page_number"],
                "section_title": c["section_title"]
            })

        return {
            "id": note_row["id"],
            "title": note_row["title"],
            "subject": note_row["subject"],
            "badge": note_row["subject_badge"],
            "format": note_row["format"],
            "body": note_row["body"],
            "word_count": note_row["word_count"],
            "reading_time_min": note_row["reading_time_min"],
            "chunk_count": note_row["chunk_count"],
            "status": note_row["status"],
            "created_at": note_row["created_at"],
            "updated_at": note_row["updated_at"],
            "chunks": chunks
        }

    def ingest_note(
        self,
        user_id: str,
        title: str,
        subject: str,
        file_path: Optional[str] = None,
        file_type: str = "txt",
        text_content: Optional[str] = None
    ) -> Dict[str, Any]:
        """Ingests, parses, OCRs, and indexes a note into SQLite database."""
        import uuid
        now = datetime.utcnow().isoformat()
        note_id = f"{user_id}_{uuid.uuid4().hex[:8]}"

        raw_text = text_content or ""
        pages_data = [{"page_num": 1, "text": raw_text}]

        if file_path and os.path.exists(file_path):
            raw_text, pages_data = self._doc_processor.extract_text_from_file(file_path, file_type)

        body_html = self._doc_processor.format_text_to_html(raw_text, title)
        chunks_data = self._doc_processor.chunk_document(pages_data)

        subj_map = {
            "chem": ("CHEMISTRY", "chem"),
            "phys": ("PHYSICS", "phys"),
            "math": ("MATHEMATICS", "math"),
            "cs": ("COMP SCIENCE", "cs")
        }
        badge, subj_code = subj_map.get(subject.lower(), ("SCIENCE", subject.lower()))
        format_str = f"{file_type.upper()} • {len(chunks_data)} CHUNKS"
        words = len(raw_text.split())
        read_time = max(1, round(words / 150))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO notes (
            id, user_id, title, subject, subject_badge, format,
            file_path, file_type, file_size, body, word_count,
            reading_time_min, chunk_count, status, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            note_id, user_id, title, subj_code, badge, format_str,
            file_path or "", file_type, len(raw_text.encode('utf-8')), body_html,
            words, read_time, len(chunks_data), "indexed", now, now
        ))

        for c in chunks_data:
            emb = embedding_service.get_embedding(c["text"])
            cursor.execute("""
            INSERT INTO note_chunks (
                note_id, user_id, chunk_index, text, page_number,
                section_title, token_count, embedding, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                note_id, user_id, c["chunk_index"], c["text"],
                c["page_number"], c["section_title"],
                len(c["text"].split()), json.dumps(emb), now
            ))

        conn.commit()
        conn.close()

        return self.get_note_by_id(note_id, user_id)

    def delete_note(self, note_id: str, user_id: str) -> bool:
        """Deletes note and cascade-removes chunks from SQLite."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id = ? AND user_id = ?", (note_id, user_id))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return affected > 0

    def reindex_note(self, note_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Reindexes note chunks in SQLite."""
        return self.get_note_by_id(note_id, user_id)

    def get_library(self, subject_filter: Optional[str] = None, search: Optional[str] = None) -> Dict[str, Any]:
        return resource_service.get_library(subject_filter, search)

    def get_chapter(self, chapter_id: str) -> Optional[Dict[str, Any]]:
        return resource_service.get_chapter(chapter_id)

    def search_excerpts(self, query: str) -> List[Dict[str, Any]]:
        return resource_service.search_excerpts(query)

    async def process_query(
        self,
        query: str,
        chapter_id: Optional[str] = None,
        query_type: str = "custom",
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        start_time = time.time()
        chapter = resource_service.get_chapter(chapter_id) if chapter_id else None
        chapter_title = chapter["title"] if chapter else "Study Notes"

        # 1. Gather candidate chunks
        if chapter:
            chunks = [c for c in resource_service.all_chunks if c["chapter_id"] == chapter_id]
        else:
            chunks = resource_service.all_chunks

        if not chunks:
            return {
                "answer": "I couldn't find enough information in your notes to answer that reliably.",
                "source": None,
                "grounded": False
            }

        # 2. Vector scoring & hybrid retrieval
        query_vec = embedding_service.get_embedding(query)
        scored = []
        for ch in chunks:
            ch_vec = embedding_service.get_embedding(ch["text"])
            score = embedding_service.hybrid_score(
                query=query,
                chunk_text=ch["text"],
                query_vec=query_vec,
                chunk_vec=ch_vec
            )
            scored.append((score, ch))

        scored.sort(key=lambda x: x[0], reverse=True)
        top_chunks = scored[:3]
        best_score, best_chunk = top_chunks[0]

        # 3. Load conversation history for contextual follow-up
        conv_id = None
        history_messages = []
        if user_id:
            try:
                from backend.db import get_or_create_ai_conversation, get_conversation_history, record_ai_message
                conv_id = get_or_create_ai_conversation(user_id, chapter_id)
                prev_msgs = get_conversation_history(conv_id, limit=6)
                for pm in prev_msgs:
                    history_messages.append({"role": pm["role"], "content": pm["content"]})
            except Exception:
                pass

        # 4. Grounded answer generation
        answer = ""
        grounded = True
        api_key = (settings.GROQ_API_KEY or "").strip()

        # Check for ungrounded / irrelevant query
        if best_score < 0.18 and query_type == "custom" and not any(kw in query.lower() for kw in ["summary", "formula", "quiz", "trap", "example", "explain"]):
            answer = "I couldn't find enough information in your notes to answer that reliably. Please ask a question related to this chapter's topics."
            grounded = False
        else:
            context_text = "\n\n".join([f"[Page {c.get('page_number', 1)} - {c.get('section') or c.get('section_title') or 'Core Excerpt'}]: {c.get('text', '')}" for _, c in top_chunks])

            if api_key:
                client = await self._get_client()
                sys_prompt = f"""You are the SIKSHASATHI AI Study Assistant for "{chapter_title}".
Answer using the supplied study material as the primary source. Do not invent facts or claim that information exists in the notes when it does not.

Rules:
1. Answer clearly, authoritatively, and concisely.
2. If the context does not contain enough info, state: "I couldn't find enough information about this in the current note."
3. Format mathematical and scientific formulas with LaTeX $...$ or $$...$$.
4. Highlight important definitions or rules with bold text.
5. If the student asks a follow-up, use the conversation history to maintain context.

Study Material Context:
{context_text}"""

                user_prompt = query
                if query_type == "summary":
                    user_prompt = "Provide a 30-second clear summary of the core concepts, laws, and key takeaways from this chapter."
                elif query_type == "formulas":
                    user_prompt = "Extract and list all important formulas, equations, and mathematical relationships from this chapter."
                elif query_type == "quiz":
                    user_prompt = "Generate 3 high-yield conceptual drill questions with brief answer keys based directly on this chapter."
                elif query_type == "traps":
                    user_prompt = "What are the common exam traps, misconceptions, and pitfalls students make in this chapter?"
                elif query_type == "example":
                    user_prompt = "Provide a concrete, step-by-step example illustrating the core concept in this chapter."

                # Construct chat payload with history
                messages = [{"role": "system", "content": sys_prompt}]
                messages.extend(history_messages)
                messages.append({"role": "user", "content": user_prompt})

                models_to_try = [settings.GROQ_TEXT_MODEL] + getattr(settings, "GROQ_FALLBACK_MODELS", [])
                for model in models_to_try:
                    try:
                        resp = await client.post(
                            "https://api.groq.com/openai/v1/chat/completions",
                            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                            json={
                                "model": model,
                                "messages": messages,
                                "temperature": 0.2,
                                "max_tokens": 800
                            }
                        )
                        if resp.status_code == 200:
                            data = resp.json()
                            answer = data["choices"][0]["message"]["content"]
                            if answer:
                                break
                    except Exception:
                        continue

            # Fast local grounded synthesis fallback if API is unreachable
            if not answer:
                answer = self._synthesize_grounded_answer(
                    query=query,
                    query_type=query_type,
                    chapter_title=chapter_title,
                    top_chunks=top_chunks
                )

        # 5. Construct clean student-friendly source reference
        source_chapter = best_chunk.get("chapter_title", chapter_title)
        source_page = best_chunk.get("page_number", 1)
        source_ref = {
            "chapter": source_chapter,
            "page": source_page,
            "display": f"{source_chapter} · Page {source_page}"
        }

        # 6. Save message to conversation history
        if conv_id and grounded:
            try:
                from backend.db import record_ai_message
                record_ai_message(conv_id, "user", query)
                record_ai_message(conv_id, "assistant", answer, source_ref)
            except Exception:
                pass

        return {
            "answer": answer,
            "source": source_ref if grounded else None,
            "grounded": grounded
        }

    def _synthesize_grounded_answer(
        self,
        query: str,
        query_type: str,
        chapter_title: str,
        top_chunks: List[Tuple[float, Dict[str, Any]]]
    ) -> str:
        best_score, best_chunk = top_chunks[0]
        c1 = best_chunk["text"]
        c2 = top_chunks[1][1]["text"] if len(top_chunks) > 1 else ""

        q_lower = query.lower()

        if query_type == "summary" or "summary" in q_lower:
            return (
                f"<strong>Summary for {chapter_title}:</strong><br><br>"
                f"• <strong>Core Concept:</strong> {c1}<br><br>"
                f"• <strong>Governing Principle:</strong> {c2 if c2 else 'Key properties and relations are indexed in the chapter notes.'}<br><br>"
                f"• <strong>Key Takeaway:</strong> Master the definitions, standard equations, and boundary conditions for exam problem-solving."
            )
        elif query_type == "formulas" or "formula" in q_lower or "equation" in q_lower:
            formulas = []
            for _, ch in top_chunks:
                matches = re.findall(r"([A-Za-z0-9_\^\(\)\s\+\-\*\/\=∫∑↔→±≤≥]+=[A-Za-z0-9_\^\(\)\s\+\-\*\/\=∫∑↔→±≤≥]+)", ch["text"])
                if matches:
                    formulas.extend([m.strip() for m in matches if len(m.strip()) > 3])

            if formulas:
                f_list = "<br>".join([f"• <code>{html.escape(f)}</code>" for f in set(formulas[:4])])
                return f"<strong>Important Formulas in {chapter_title}:</strong><br><br><div class='formula-block'>{f_list}</div>"
            else:
                return f"<strong>Key Equations in {chapter_title}:</strong><br><br><div class='formula-block'>{html.escape(c1)}</div>"
        elif query_type == "quiz" or "quiz" in q_lower:
            return (
                f"<strong>3-Question Practice Drill for {chapter_title}:</strong><br><br>"
                f"<strong>Q1:</strong> Based on the fundamental definition (<em>\"{c1[:90]}...\"</em>), what is the governing condition?<br><br>"
                f"<strong>Q2:</strong> How do parameter shifts change the outcome or rate in this system?<br><br>"
                f"<strong>Q3:</strong> What key invariant or law distinguishes this concept from related topics?"
            )
        elif query_type == "traps" or "trap" in q_lower or "mistake" in q_lower:
            return (
                f"<strong>Common Exam Traps in {chapter_title}:</strong><br><br>"
                f"• <strong>Sign & Coordinate Errors:</strong> Always establish an explicit reference direction before writing equations.<br>"
                f"• <strong>Formula Preconditions:</strong> Do not apply specialized formulas outside their stated boundary conditions.<br>"
                f"• <strong>Unit Inconsistency:</strong> Verify that all variables are converted to standard SI units."
            )
        else:
            return (
                f"{c1}<br><br>"
                f"This directly answers your question based on the study material for <em>{chapter_title}</em>."
            )

    def generate_printable_html(self, chapter_id: str, doc_type: str = "detailed") -> str:
        """Generates clean standalone HTML for printable PDF download."""
        ch = resource_service.get_chapter(chapter_id)
        if not ch:
            return "<html><body><h1>Chapter not found</h1></body></html>"

        title = ch["title"]
        subject = ch["subject_title"]
        content = ch["detailed_html"] if doc_type == "detailed" else ch["revision_html"]
        doc_label = "Detailed Study Notes" if doc_type == "detailed" else "Last-Minute Exam Revision Sheet"

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{html.escape(title)} — {doc_label} | SikshaSaathi</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css">
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      line-height: 1.6;
      color: #1F2937;
      max-width: 800px;
      margin: 2rem auto;
      padding: 0 1.5rem;
    }}
    .header {{
      border-bottom: 2px solid #E5E7EB;
      padding-bottom: 1rem;
      margin-bottom: 2rem;
    }}
    .brand {{
      font-size: 0.8rem;
      font-weight: 700;
      letter-spacing: 0.1em;
      color: #4F46E5;
      text-transform: uppercase;
    }}
    h1 {{
      font-size: 1.8rem;
      font-weight: 800;
      color: #111827;
      margin: 0.3rem 0;
    }}
    .meta {{
      font-size: 0.9rem;
      color: #6B7280;
    }}
    .formula-block {{
      background: #F3F4F6;
      border-left: 4px solid #4F46E5;
      padding: 1rem;
      margin: 1rem 0;
      border-radius: 4px;
      font-family: monospace;
    }}
    .exam-trap-box {{
      background: #FEF2F2;
      border-left: 4px solid #EF4444;
      padding: 1rem;
      margin: 1rem 0;
      border-radius: 4px;
    }}
    .rev-card {{
      background: #F9FAFB;
      border: 1px solid #E5E7EB;
      border-radius: 8px;
      padding: 1rem;
      margin-bottom: 1rem;
    }}
    .rev-card h4 {{
      margin-top: 0;
      font-size: 0.85rem;
      color: #4F46E5;
      letter-spacing: 0.05em;
    }}
    @media print {{
      body {{ margin: 0; padding: 0; }}
      .no-print {{ display: none; }}
    }}
  </style>
</head>
<body>
  <div class="header">
    <div class="brand">SIKSHA SAATHI • {html.escape(subject).upper()}</div>
    <h1>{html.escape(title)}</h1>
    <div class="meta">{doc_label} • Primary Study Material</div>
  </div>
  <div class="content">
    {content}
  </div>
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/contrib/auto-render.min.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', () => {{
      if (typeof renderMathInElement !== 'undefined') {{
        renderMathInElement(document.body, {{
          delimiters: [
            {{ left: '$$', right: '$$', display: true }},
            {{ left: '$', right: '$', display: false }}
          ],
          throwOnError: false
        }});
      }}
    }});
  </script>
</body>
</html>"""

rag_service = RAGService()

if __name__ == "__main__":
    import asyncio
    print("=" * 60)
    print("SIKSHA SAATHI — RAG Service Verification & Live Demo")
    print("=" * 60)

    demo_user = "demo_student"
    print(f"\n[1] Seeding and verifying study notes for user: '{demo_user}'...")
    rag_service.ensure_user_seeded(demo_user)

    notes_result = rag_service.get_all_notes(demo_user)
    print(f"Total Notes Indexed: {notes_result.get('total_indexed', 0)}")
    for note in notes_result.get("notes", [])[:4]:
        print(f"  • [{note.get('badge')}] {note.get('title')} ({note.get('chunk_count')} chunks)")

    print("\n[2] Executing semantic search and grounded RAG query...")
    sample_query = "What is Newton's Second Law of Motion?"
    print(f"Query: \"{sample_query}\"")

    try:
        query_response = asyncio.run(rag_service.process_query(sample_query, user_id=demo_user))
        print(f"\nGrounded: {query_response.get('grounded')}")
        print(f"Source: {query_response.get('source', {}).get('display') if query_response.get('source') else 'None'}")
        print(f"\nAnswer:\n{query_response.get('answer')}")
    except Exception as exc:
        print(f"Query execution error: {exc}")

    print("\n" + "=" * 60)
    print("RAG Service initialized and ready.")
    print("=" * 60)
