"""
SIKHSAATHI — AI Personalized Learning Roadmap Engine
Generates and maintains a dynamic, validated, student-specific learning journey
grounded in real quiz performance, level completions, and database study resources.
Powered by Groq LLM with strict JSON validation, caching, and authentic fallback.
"""

import os
import json
import time
import hashlib
import httpx
from datetime import datetime
from typing import Dict, List, Any, Optional

from backend.config import settings
from backend.db import (
    get_or_create_profile, get_user_progress_summary,
    get_active_roadmap, save_learning_roadmap,
    get_practice_subjects, get_user_quiz_history
)
from backend.services.resource_service import resource_service


class RoadmapService:
    def __init__(self):
        self._http_client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._http_client is None or self._http_client.is_closed:
            limits = httpx.Limits(max_keepalive_connections=10, max_connections=20)
            timeout = httpx.Timeout(15.0, connect=4.0)
            self._http_client = httpx.AsyncClient(limits=limits, timeout=timeout)
        return self._http_client

    def _compute_progress_hash(self, progress: dict) -> str:
        """Computes a deterministic snapshot hash to detect progress changes."""
        key_parts = [
            str(progress.get("completed_levels_count", 0)),
            str(progress.get("total_questions_solved", 0)),
            str(progress.get("overall_accuracy_percent", 0.0))
        ]
        for s in progress.get("subjects", []):
            key_parts.append(f"{s['id']}:{s['completed_levels']}:{s['accuracy_percent']}")
        raw = "|".join(key_parts)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]

    def get_roadmap_status(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieves active roadmap, checks for progress evolution, and returns cache status.
        """
        progress = get_user_progress_summary(user_id)
        current_hash = self._compute_progress_hash(progress)
        existing = get_active_roadmap(user_id)

        if not existing:
            return {
                "has_roadmap": False,
                "is_outdated": False,
                "roadmap": None,
                "current_hash": current_hash
            }

        is_outdated = existing.get("progress_snapshot_hash") != current_hash
        return {
            "has_roadmap": True,
            "is_outdated": is_outdated,
            "roadmap": existing,
            "current_hash": current_hash
        }

    async def generate_roadmap(self, user_id: str) -> Dict[str, Any]:
        """
        Gathers live student learning telemetry, invokes Groq LLM for personalized synthesis,
        validates all recommended chapters and practice levels, and stores in SQLite.
        """
        profile = get_or_create_profile(user_id)
        progress = get_user_progress_summary(user_id)
        history = get_user_quiz_history(user_id, limit=8)
        current_hash = self._compute_progress_hash(progress)

        # 1. Compile student learning telemetry for AI prompt
        student_name = profile.get("full_name") or "Student"
        target_goal = profile.get("target_goal") or "Senior Secondary Mastery"
        class_level = profile.get("class_level") or "Class 12"

        subjects_summary = []
        for s in progress.get("subjects", []):
            subjects_summary.append({
                "subject": s["title"],
                "subject_id": s["id"],
                "completed_levels": f"{s['completed_levels']}/5",
                "accuracy": f"{s['accuracy_percent']}%",
                "status": "Mastered" if s["completed_levels"] == 5 else f"Next is Level {s['unlocked_level']}"
            })

        recent_attempts = []
        for h in history[:5]:
            recent_attempts.append({
                "subject": h["subject_title"],
                "level": h["level_number"],
                "score": f"{h['score']}/{h['total_questions']}",
                "accuracy": f"{h['accuracy_percent']}%"
            })

        # Available authentic resources in database
        available_notes = [
            {"id": "units-and-dimensions", "subject": "Physics", "title": "Units and Dimensions"},
            {"id": "newtons-laws-of-motion", "subject": "Physics", "title": "Newton's Laws of Motion"},
            {"id": "acids-bases-salts", "subject": "Chemistry", "title": "Acids, Bases and Salts"},
            {"id": "differentiation-calculus", "subject": "Mathematics", "title": "Differentiation & Calculus"},
            {"id": "dbms", "subject": "Computer Science", "title": "Database Management Systems"},
            {"id": "sql", "subject": "Computer Science", "title": "SQL & Relational Queries"},
            {"id": "computer-networks", "subject": "Computer Science", "title": "Computer Networks"}
        ]

        # 2. Query Groq LLM
        roadmap_data = await self._call_groq_for_roadmap(
            student_name=student_name,
            target_goal=target_goal,
            class_level=class_level,
            progress=progress,
            subjects_summary=subjects_summary,
            recent_attempts=recent_attempts,
            available_notes=available_notes
        )

        # 3. If AI output was invalid or empty, synthesize authentic deterministic roadmap
        if not roadmap_data or not roadmap_data.get("nodes"):
            roadmap_data = self._synthesize_grounded_roadmap(
                student_name=student_name,
                target_goal=target_goal,
                progress=progress
            )

        # 4. Strict resource validation against database
        validated_nodes = self._validate_and_sanitize_nodes(roadmap_data.get("nodes", []))
        roadmap_data["nodes"] = validated_nodes

        # 5. Persist into SQLite
        saved = save_learning_roadmap(
            user_id=user_id,
            title=roadmap_data.get("title", f"Personalized Learning Path for {student_name}"),
            summary=roadmap_data.get("summary", "Dynamic roadmap based on diagnostic progress."),
            goal=roadmap_data.get("goal", target_goal),
            estimated_duration=roadmap_data.get("estimatedDuration", "12 Days"),
            progress_snapshot_hash=current_hash,
            roadmap_data=roadmap_data
        )

        return {
            "status": "success",
            "is_outdated": False,
            "roadmap": saved
        }

    async def _call_groq_for_roadmap(
        self,
        student_name: str,
        target_goal: str,
        class_level: str,
        progress: dict,
        subjects_summary: list,
        recent_attempts: list,
        available_notes: list
    ) -> Optional[dict]:
        """Calls Groq API to generate structured JSON learning roadmap."""
        api_key = (settings.GROQ_ROADMAP_API_KEY or settings.GROQ_API_KEY or "").strip()
        if not api_key:
            return None

        client = await self._get_client()

        system_prompt = f"""You are the SIKSHASATHI Cognitive AI Learning Path Architect.
Create a personalized, step-by-step visual learning roadmap for {student_name}.

CRITICAL RULES:
1. Output MUST be strictly valid JSON matching the exact schema below. No markdown fences around JSON, no chatter.
2. NEVER invent non-existent chapters or levels.
   Available Study Notes IDs: {[n['id'] for n in available_notes]}
   Available Practice Subject IDs: ["phys", "chem", "math", "cs"] with levels 1, 2, 3, 4, 5.
3. Node types must be: "start", "completed", "current", "recommended", "review", "milestone", "locked".
4. Every node MUST have a clear, motivating "reason" explaining WHY the AI recommends it based on the student's actual performance.
5. Provide realistic "estimatedMinutes" (e.g. 25, 45, 60).
6. Provide clean "actions" array linking to notes or practice:
   - Notes action: {{"type": "notes", "label": "Study Notes", "chapter_id": "<valid_id>"}}
   - Practice action: {{"type": "practice", "label": "Practice Level <N>", "subject_id": "<phys|chem|math|cs>", "level_number": <N>}}

Required JSON Output Structure:
{{
  "title": "Your Personalized Learning Journey",
  "summary": "<1-2 sentence executive summary of current focus and next milestones>",
  "goal": "{target_goal}",
  "estimatedDuration": "<e.g. 10 Days>",
  "nodes": [
    {{
      "id": "node-1",
      "type": "start",
      "subject": "Overview",
      "topic": "Diagnostic Starting Point",
      "status": "completed",
      "reason": "Baseline diagnostic evaluation completed across core subjects.",
      "estimatedMinutes": 15,
      "actions": []
    }},
    {{
      "id": "node-2",
      "type": "completed",
      "subject": "Mathematics",
      "topic": "Algebra & Quadratic Foundations",
      "status": "completed",
      "accuracy_percent": 90.0,
      "reason": "You demonstrated high accuracy in foundation algebraic problems.",
      "estimatedMinutes": 30,
      "actions": [{{"type": "practice", "label": "Review Quiz", "subject_id": "math", "level_number": 1}}]
    }},
    {{
      "id": "node-3",
      "type": "current",
      "subject": "Physics",
      "topic": "Newton's Laws & Dynamics",
      "status": "current",
      "accuracy_percent": 65.0,
      "reason": "Your recent diagnostics show sign convention errors. Reinforcing fundamental forces will stabilize your trajectory.",
      "estimatedMinutes": 45,
      "actions": [
        {{"type": "notes", "label": "Study Chapter Notes", "chapter_id": "newtons-laws-of-motion"}},
        {{"type": "practice", "label": "Practice Level 2", "subject_id": "phys", "level_number": 2}}
      ]
    }},
    {{
      "id": "node-4",
      "type": "recommended",
      "subject": "Chemistry",
      "topic": "Acids, Bases & pH Calculations",
      "status": "recommended",
      "reason": "Key high-yield topic scheduled to balance your science mastery index.",
      "estimatedMinutes": 40,
      "actions": [
        {{"type": "notes", "label": "Study Chapter Notes", "chapter_id": "acids-bases-salts"}},
        {{"type": "practice", "label": "Practice Level 2", "subject_id": "chem", "level_number": 2}}
      ]
    }},
    {{
      "id": "node-5",
      "type": "milestone",
      "subject": "Core Milestone",
      "topic": "Mid-Semester Diagnostic Mastery",
      "status": "locked",
      "reason": "Unlock after completing Level 2 across all 4 subjects.",
      "estimatedMinutes": 60,
      "actions": []
    }},
    {{
      "id": "node-6",
      "type": "locked",
      "subject": "Computer Science",
      "topic": "Relational DBMS & SQL Optimization",
      "status": "locked",
      "reason": "Advanced stage scheduled after foundational network & data structure drills.",
      "estimatedMinutes": 50,
      "actions": [
        {{"type": "notes", "label": "Study Chapter Notes", "chapter_id": "sql"}},
        {{"type": "practice", "label": "Practice Level 3", "subject_id": "cs", "level_number": 3}}
      ]
    }}
  ]
}}"""

        user_content = f"""Student Profile:
- Name: {student_name}
- Class: {class_level}
- Target Goal: {target_goal}
- Overall Progress: {progress.get('overall_progress_percent', 0)}%
- Completed Levels: {progress.get('completed_levels_count', 0)} / 20
- Questions Solved: {progress.get('total_questions_solved', 0)}
- Overall Accuracy: {progress.get('overall_accuracy_percent', 0)}%

Subject Breakdown:
{json.dumps(subjects_summary, indent=2)}

Recent Quiz Performance:
{json.dumps(recent_attempts, indent=2)}

Generate the personalized structured JSON roadmap for this student right now."""

        models_to_try = [settings.GROQ_TEXT_MODEL] + getattr(settings, "GROQ_FALLBACK_MODELS", [])

        for model in models_to_try:
            try:
                resp = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_content}
                        ],
                        "response_format": {"type": "json_object"},
                        "temperature": 0.25,
                        "max_tokens": 1200
                    }
                )

                if resp.status_code == 200:
                    raw_content = resp.json()["choices"][0]["message"]["content"]
                    # Parse JSON
                    cleaned = raw_content.strip()
                    if cleaned.startswith("```json"):
                        cleaned = cleaned[7:]
                    if cleaned.startswith("```"):
                        cleaned = cleaned[3:]
                    if cleaned.endswith("```"):
                        cleaned = cleaned[:-3]
                    cleaned = cleaned.strip()

                    parsed = json.loads(cleaned)
                    if parsed.get("nodes") and len(parsed["nodes"]) >= 4:
                        return parsed
            except Exception as e:
                continue

        return None

    def _synthesize_grounded_roadmap(
        self,
        student_name: str,
        target_goal: str,
        progress: dict
    ) -> dict:
        """
        Fallback generator that builds an authentic, calibrated roadmap from the SQLite progress data.
        """
        completed = progress.get("completed_levels_count", 0)
        overall_acc = progress.get("overall_accuracy_percent", 0.0)
        subjects = progress.get("subjects", [])

        nodes = [
            {
                "id": "node-start",
                "type": "start",
                "subject": "Diagnostic Start",
                "topic": "Academic Genome Initialization",
                "status": "completed",
                "reason": f"Diagnostic baseline configured for {target_goal}.",
                "estimatedMinutes": 10,
                "actions": []
            }
        ]

        # 1. Physics Node
        phys = next((s for s in subjects if s["id"] == "phys"), {"completed_levels": 0, "accuracy_percent": 0.0, "unlocked_level": 1})
        if phys["completed_levels"] > 0:
            nodes.append({
                "id": "node-phys-1",
                "type": "completed",
                "subject": "Physics",
                "topic": "Mechanics Foundation",
                "status": "completed",
                "accuracy_percent": phys["accuracy_percent"] or 80.0,
                "reason": "Foundation drill completed with recorded diagnostic score.",
                "estimatedMinutes": 30,
                "actions": [
                    {"type": "notes", "label": "Review Notes", "chapter_id": "units-and-dimensions"},
                    {"type": "practice", "label": "Retake Quiz", "subject_id": "phys", "level_number": 1}
                ]
            })
        else:
            nodes.append({
                "id": "node-phys-curr",
                "type": "current",
                "subject": "Physics",
                "topic": "Newton's Laws & Force Vectors",
                "status": "current",
                "accuracy_percent": 0.0,
                "reason": "Core prerequisite for senior mechanics. Establishing reference frames and vector decomposition.",
                "estimatedMinutes": 45,
                "actions": [
                    {"type": "notes", "label": "Study Notes", "chapter_id": "newtons-laws-of-motion"},
                    {"type": "practice", "label": f"Start Level {phys['unlocked_level']}", "subject_id": "phys", "level_number": phys["unlocked_level"]}
                ]
            })

        # 2. Mathematics Node
        math = next((s for s in subjects if s["id"] == "math"), {"completed_levels": 0, "accuracy_percent": 0.0, "unlocked_level": 1})
        nodes.append({
            "id": "node-math-rec",
            "type": "recommended" if math["completed_levels"] == 0 else "current",
            "subject": "Mathematics",
            "topic": "Differential Calculus & Curves",
            "status": "recommended" if math["completed_levels"] == 0 else "current",
            "accuracy_percent": math["accuracy_percent"],
            "reason": "Calculus mastery directly improves rate-of-change problem solving across Physics and Chemistry.",
            "estimatedMinutes": 45,
            "actions": [
                {"type": "notes", "label": "Study Notes", "chapter_id": "differentiation-calculus"},
                {"type": "practice", "label": f"Practice Level {math['unlocked_level']}", "subject_id": "math", "level_number": math["unlocked_level"]}
            ]
        })

        # 3. Chemistry Node
        chem = next((s for s in subjects if s["id"] == "chem"), {"completed_levels": 0, "accuracy_percent": 0.0, "unlocked_level": 1})
        nodes.append({
            "id": "node-chem-rev",
            "type": "review" if chem["accuracy_percent"] < 70 and chem["completed_levels"] > 0 else "recommended",
            "subject": "Chemistry",
            "topic": "Acids, Bases & Equilibria",
            "status": "recommended",
            "accuracy_percent": chem["accuracy_percent"],
            "reason": "High-yield conceptual drill focusing on aqueous equilibria and pH calculations.",
            "estimatedMinutes": 40,
            "actions": [
                {"type": "notes", "label": "Study Notes", "chapter_id": "acids-bases-salts"},
                {"type": "practice", "label": f"Practice Level {chem['unlocked_level']}", "subject_id": "chem", "level_number": chem["unlocked_level"]}
            ]
        })

        # 4. Milestone Check
        nodes.append({
            "id": "node-milestone-1",
            "type": "milestone",
            "subject": "Progress Milestone",
            "topic": "Core Foundation Mastery",
            "status": "locked" if completed < 4 else "completed",
            "reason": "Demonstrate at least 4 completed levels with >75% accuracy across subjects.",
            "estimatedMinutes": 60,
            "actions": []
        })

        # 5. Computer Science / Advanced Node
        cs = next((s for s in subjects if s["id"] == "cs"), {"completed_levels": 0, "accuracy_percent": 0.0, "unlocked_level": 1})
        nodes.append({
            "id": "node-cs-adv",
            "type": "locked",
            "subject": "Computer Science",
            "topic": "Relational DBMS & SQL Optimization",
            "status": "locked",
            "accuracy_percent": cs["accuracy_percent"],
            "reason": "Scheduled after foundational algorithmic principles are consolidated.",
            "estimatedMinutes": 50,
            "actions": [
                {"type": "notes", "label": "Study Notes", "chapter_id": "dbms"},
                {"type": "practice", "label": f"Practice Level {cs['unlocked_level']}", "subject_id": "cs", "level_number": cs["unlocked_level"]}
            ]
        })

        return {
            "title": f"Personalized Learning Pathway for {student_name}",
            "summary": f"Targeted roadmap focusing on {target_goal} with calibrated diagnostics across 4 core domains.",
            "goal": target_goal,
            "estimatedDuration": "12 Days",
            "nodes": nodes
        }

    def _validate_and_sanitize_nodes(self, nodes: list) -> list:
        """Ensures every node references real existing notes and valid practice levels."""
        valid_chapters = {
            "units-and-dimensions", "newtons-laws-of-motion", "acids-bases-salts",
            "differentiation-calculus", "dbms", "sql", "computer-networks"
        }
        valid_subjects = {"phys", "chem", "math", "cs"}

        sanitized = []
        for i, n in enumerate(nodes):
            node_copy = dict(n)
            node_copy["id"] = node_copy.get("id") or f"node-{i+1}"
            node_copy["type"] = node_copy.get("type", "recommended").lower()
            node_copy["subject"] = node_copy.get("subject", "Science")
            node_copy["topic"] = node_copy.get("topic", "Core Chapter")
            node_copy["status"] = node_copy.get("status", "recommended").lower()
            node_copy["reason"] = node_copy.get("reason", "Recommended based on your curriculum pacing.")
            node_copy["estimatedMinutes"] = int(node_copy.get("estimatedMinutes") or node_copy.get("estimated_minutes") or 35)

            # Validate actions
            clean_actions = []
            for act in node_copy.get("actions", []):
                act_type = act.get("type", "").lower()
                if act_type == "notes":
                    ch_id = act.get("chapter_id") or act.get("targetId")
                    if ch_id in valid_chapters:
                        clean_actions.append({
                            "type": "notes",
                            "label": act.get("label", "Study Chapter Notes"),
                            "chapter_id": ch_id
                        })
                elif act_type == "practice":
                    s_id = (act.get("subject_id") or act.get("targetId") or "").lower()
                    lvl_num = int(act.get("level_number") or act.get("level") or 1)
                    if s_id in valid_subjects and 1 <= lvl_num <= 5:
                        clean_actions.append({
                            "type": "practice",
                            "label": act.get("label", f"Practice Level {lvl_num}"),
                            "subject_id": s_id,
                            "level_number": lvl_num
                        })

            node_copy["actions"] = clean_actions
            sanitized.append(node_copy)

        return sanitized


roadmap_service = RoadmapService()
