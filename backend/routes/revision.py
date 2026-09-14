"""
SIKSHA SAATHI — Forgetting Prediction & Smart Revision API Router
Provides authenticated endpoints for:
- Revision overview & queue (Needs Attention, Review Soon, Doing Well)
- Topic smart path detail with real practice questions
- Session start & session completion with telemetry persistence
- Real revision history from SQLite
"""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Header, HTTPException, Query
from pydantic import BaseModel

from backend.db import (
    get_user_from_session, get_user_by_id, get_user_by_email,
    get_user_revision_history
)
from backend.services.revision_service import revision_service

router = APIRouter(tags=["Smart Revision & Forgetting Prediction"])


class RevisionCompleteRequest(BaseModel):
    topic: str
    subject_id: str
    duration_minutes: Optional[float] = 15.0
    steps_total: Optional[int] = 4
    steps_completed: Optional[int] = 4
    score: Optional[int] = 0
    total_questions: Optional[int] = 0
    review_mode: Optional[str] = "standard"
    resources_used: Optional[List[str]] = []


def _resolve_user(
    authorization: Optional[str] = None,
    x_user_id: Optional[str] = None,
    x_auth_token: Optional[str] = None
) -> dict:
    """Extracts authenticated user identity from Bearer token or custom headers."""
    token = None
    if isinstance(x_auth_token, str) and x_auth_token.strip():
        token = x_auth_token.strip()
    elif isinstance(authorization, str) and "Bearer " in authorization:
        token = authorization.replace("Bearer ", "").strip()

    if token == "token_demo_sandbox_session" or (not token and x_user_id == "usr_demo_sandbox"):
        return {
            "id": "usr_demo_sandbox",
            "full_name": "Guest Learner (Demo)",
            "email": "demo@sikshasaathi.sandbox",
            "role": "student",
            "class_grade": "Class 12 • Science (Demo Sandbox)",
            "target_goal": "Platform Exploration",
            "bio": "Exploring Siksha Saathi features in sandbox mode.",
            "institution": "Sandbox Environment",
            "subject": "Physics",
            "avatar_url": "",
            "is_demo": True
        }

    if token and token.startswith("ey") and token.count(".") == 2:
        try:
            from backend.services.supabase_service import verify_supabase_token, is_supabase_configured
            if is_supabase_configured():
                u = verify_supabase_token(token)
                if u:
                    return {
                        "id": str(u["id"]),
                        "full_name": u.get("full_name", "Student"),
                        "email": u.get("email"),
                        "role": u.get("role", "student"),
                        "class_grade": u.get("class_grade", "Class 12"),
                        "is_demo": False
                    }
        except Exception:
            pass

    if token:
        user = get_user_from_session(token)
        if user:
            return user

    raise HTTPException(
        status_code=401,
        detail="Active authentication session required."
    )


@router.get("/api/revision/overview")
@router.get("/api/student/revision/overview")
async def get_revision_overview_endpoint(
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """
    Returns authentic forgetting prediction telemetry, today's top priority topic,
    categorized urgency queues, and recent revision history.
    """
    user = _resolve_user(authorization, x_user_id, x_auth_token)
    data = revision_service.get_revision_overview(user["id"])
    data["user"] = {
        "id": user["id"],
        "name": user.get("full_name", "Student")
    }
    return data


@router.get("/api/revision/topic/{subject_id}/{topic}")
@router.get("/api/student/revision/topic/{subject_id}/{topic}")
async def get_topic_smart_path_endpoint(
    subject_id: str,
    topic: str,
    time_budget: int = Query(15, ge=5, le=45),
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """
    Returns the adaptive Smart Revision sequence, verified resources,
    and actual practice questions for interactive revision session execution.
    """
    user = _resolve_user(authorization, x_user_id, x_auth_token)
    return await revision_service.get_topic_smart_path_detail(
        user_id=user["id"],
        subject_id=subject_id.lower(),
        topic_name=topic,
        time_budget_min=time_budget
    )


@router.post("/api/revision/topic/{subject_id}/{topic}/generate-questions")
@router.post("/api/student/revision/topic/{subject_id}/{topic}/generate-questions")
async def generate_topic_questions_endpoint(
    subject_id: str,
    topic: str,
    count: int = Query(3, ge=1, le=5),
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """
    Generates fresh, unique, topic-specific question variants on the fly
    using Groq AI with parametric fallbacks and persists them to SQLite.
    """
    user = _resolve_user(authorization, x_user_id, x_auth_token)
    from backend.services.question_engine import dynamic_question_engine

    questions = await dynamic_question_engine.get_topic_questions(
        subject_id=subject_id.lower(),
        topic=topic,
        count=count,
        user_id=user["id"],
        force_new=True
    )
    return {
        "status": "success",
        "subject_id": subject_id.lower(),
        "topic": topic,
        "questions": questions
    }


@router.post("/api/revision/session/complete")
@router.post("/api/student/revision/session/complete")
async def complete_revision_session_endpoint(
    payload: RevisionCompleteRequest,
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """
    Persists a completed revision session to SQLite, updates telemetry,
    recalculates memory stability & retention, and returns the updated state.
    """
    user = _resolve_user(authorization, x_user_id, x_auth_token)
    try:
        return revision_service.complete_session(user["id"], payload.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to persist revision session: {str(e)}")


@router.get("/api/revision/history")
@router.get("/api/student/revision/history")
async def get_revision_history_endpoint(
    limit: int = Query(20, ge=1, le=100),
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """
    Returns full history of completed revision sessions for the authenticated student.
    """
    user = _resolve_user(authorization, x_user_id, x_auth_token)
    history = get_user_revision_history(user["id"], limit=limit)
    return {
        "status": "success",
        "user_id": user["id"],
        "history": history
    }
