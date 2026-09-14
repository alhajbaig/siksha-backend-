"""
SIKHSAATHI — Notes Study Library API Routes
Clean student-facing endpoints for the Notes page.
Delegates to resource_service for content and rag_service for AI queries.
"""

import os
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

from backend.services.resource_service import resource_service, RESOURCES_DIR
from backend.services.rag_service import rag_service

router = APIRouter(prefix="/api/notes", tags=["Notes Study Library"])


# ---------- Pydantic Models ----------

class AskRequest(BaseModel):
    query: str
    chapter_id: Optional[str] = None
    query_type: Optional[str] = "custom"


# ---------- Library Endpoints ----------

@router.get("/library")
async def get_library(
    subject: Optional[str] = Query(None, description="Filter by subject: phys, chem, math, cs"),
    search: Optional[str] = Query(None, description="Search query across notes")
):
    """Returns the study library: subject counts and chapter cards."""
    return resource_service.get_library(subject_filter=subject, search_query=search)


@router.get("/search")
async def search_notes(
    q: str = Query(..., description="Search query")
):
    """Searches across all notes and returns excerpts with chapter references."""
    results = resource_service.search_excerpts(q)
    return {"status": "success", "results": results}


# ---------- Chapter Endpoints ----------

@router.get("/chapter/{chapter_id}")
async def get_chapter(chapter_id: str):
    """Returns full chapter data including all study modes."""
    chapter = resource_service.get_chapter(chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    return {
        "status": "success",
        "chapter": {
            "id": chapter["id"],
            "title": chapter["title"],
            "subject": chapter["subject"],
            "subject_title": chapter["subject_title"],
            "source_file": chapter["source_file"],
            "reading_time_min": chapter["reading_time_min"],
            "word_count": chapter["word_count"],
            "detailed_html": chapter["detailed_html"],
            "toc": chapter["toc"],
            "revision_html": chapter["revision_html"],
            "flashcards": chapter["flashcards"],
            "flow_data": chapter["flow_data"],
            "mindmap_data": chapter["mindmap_data"],
            "has_handwritten": chapter["has_handwritten"],
            "chunks_count": chapter["chunks_count"]
        }
    }


# ---------- AI / RAG Endpoints ----------

def _resolve_user_id(
    authorization: Optional[str] = None,
    x_user_id: Optional[str] = None,
    x_auth_token: Optional[str] = None
) -> Optional[str]:
    from backend.db import get_user_from_session
    token = None
    if isinstance(x_auth_token, str) and x_auth_token.strip():
        token = x_auth_token.strip()
    elif isinstance(authorization, str) and "Bearer " in authorization:
        token = authorization.replace("Bearer ", "").strip()

    if token == "token_demo_sandbox_session" or (not token and x_user_id == "usr_demo_sandbox"):
        return "usr_demo_sandbox"

    if token and token.startswith("ey") and token.count(".") == 2:
        try:
            from backend.services.supabase_service import verify_supabase_token, is_supabase_configured
            if is_supabase_configured():
                u = verify_supabase_token(token)
                if u:
                    return str(u["id"])
        except Exception:
            pass

    if token:
        user = get_user_from_session(token)
        if user:
            return user["id"]

    return None


@router.post("/ask")
async def ask_ai(
    payload: AskRequest,
    authorization: Optional[str] = None,
    x_user_id: Optional[str] = None,
    x_auth_token: Optional[str] = None
):
    """RAG-powered question answering, grounded in chapter content with multi-turn history."""
    user_id = _resolve_user_id(authorization, x_user_id, x_auth_token)
    result = await rag_service.process_query(
        query=payload.query,
        chapter_id=payload.chapter_id,
        query_type=payload.query_type or "custom",
        user_id=user_id
    )
    return {"status": "success", **result}


# ---------- Download Endpoints ----------

@router.get("/download/{chapter_id}", response_class=HTMLResponse)
async def download_notes(
    chapter_id: str,
    type: str = Query("detailed", description="Download type: detailed or revision")
):
    """Returns printable HTML for Detailed Notes or Revision Sheet."""
    doc_type = "detailed" if type != "revision" else "revision"
    html_content = rag_service.generate_printable_html(chapter_id, doc_type)
    if "Chapter not found" in html_content:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return HTMLResponse(content=html_content)


@router.get("/handwritten/{chapter_id}")
async def download_handwritten(chapter_id: str):
    """Serves the original PDF source file for download."""
    chapter = resource_service.get_chapter(chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    source_file = chapter.get("source_file", "")
    file_path = os.path.join(RESOURCES_DIR, source_file)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Source file not available")

    return FileResponse(
        path=file_path,
        filename=source_file,
        media_type="application/pdf"
    )
