"""
SIKSHA SAATHI — Emergency Mode API Router
Provides authenticated endpoints for:
- Student context retrieval (profile, subjects, progress, resources)
- Emergency plan generation (evidence-backed, time-constrained)
- Session completion with ecosystem feedback
- Session retrieval for resume/review
"""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Header, HTTPException, Query
from pydantic import BaseModel

from backend.db import (
    get_user_from_session, get_user_by_id, get_user_by_email,
    get_emergency_session
)
from backend.services.emergency_service import emergency_service

router = APIRouter(prefix="/api/emergency", tags=["Emergency Mode"])


# ---------- Request Models ----------

class EmergencyPlanRequest(BaseModel):
    available_minutes: int
    subject_focus: Optional[str] = "all"
    situation: Optional[str] = "auto"
    exam_name: Optional[str] = ""
    exam_date: Optional[str] = ""


class EmergencyCompleteRequest(BaseModel):
    session_id: str
    steps_completed: Optional[int] = 0
    topics_covered: Optional[List[str]] = []
    performance: Optional[Dict[str, Any]] = {}
    self_ratings: Optional[Dict[str, Any]] = {}
    skipped_steps: Optional[List[int]] = []


# ---------- Auth Helper ----------

def _resolve_user(
    authorization: Optional[str] = None,
    x_user_id: Optional[str] = None,
    x_auth_token: Optional[str] = None
) -> dict:
    """Resolves authenticated student from Bearer token or custom headers."""
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


# ---------- Endpoints ----------

@router.get("/context")
async def get_emergency_context(
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """
    Returns the authenticated student's Emergency Mode context:
    profile, subjects with progress, calibration state, situation analysis, scenarios.
    All data from real database queries. No fabrication.
    """
    user = _resolve_user(authorization, x_user_id, x_auth_token)
    try:
        context = emergency_service.get_student_context(user["id"])
        return context
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load emergency context: {str(e)}")


@router.post("/plan")
async def build_emergency_plan(
    payload: EmergencyPlanRequest,
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """
    Builds a time-constrained, evidence-backed emergency rescue plan.
    Hard constraint: TOTAL PLAN TIME <= available_minutes.
    Employs Situation Intelligence to adjust prioritization strategy.
    """
    user = _resolve_user(authorization, x_user_id, x_auth_token)

    if payload.available_minutes < 5:
        raise HTTPException(status_code=400, detail="Minimum 5 minutes required.")
    if payload.available_minutes > 300:
        raise HTTPException(status_code=400, detail="Maximum 5 hours (300 minutes) supported.")

    try:
        plan = emergency_service.build_plan(
            user_id=user["id"],
            available_minutes=payload.available_minutes,
            subject_focus=payload.subject_focus or "all",
            situation=payload.situation or "auto",
            exam_name=payload.exam_name or "",
            exam_date=payload.exam_date or ""
        )
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to build emergency plan: {str(e)}")


@router.post("/session/complete")
async def complete_emergency_session(
    payload: EmergencyCompleteRequest,
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """
    Completes an emergency session:
    - Persists measured outcomes
    - Feeds completed topics back into revision_sessions
    - Generates ecosystem handoff guidance
    """
    user = _resolve_user(authorization, x_user_id, x_auth_token)
    try:
        perf = payload.performance or {}
        if payload.self_ratings:
            perf["self_ratings"] = payload.self_ratings
        if payload.skipped_steps:
            perf["skipped_steps"] = payload.skipped_steps

        result = emergency_service.complete_session(
            user_id=user["id"],
            session_id=payload.session_id,
            steps_completed=payload.steps_completed or 0,
            topics_covered=payload.topics_covered or [],
            performance=perf
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to complete session: {str(e)}")


@router.get("/session/{session_id}")
async def get_session(
    session_id: str,
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """
    Retrieves an emergency session for resume or review.
    Enforces student ownership isolation.
    """
    user = _resolve_user(authorization, x_user_id, x_auth_token)
    session = get_emergency_session(session_id, user["id"])
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or access denied.")
    return {"status": "success", "session": session}
