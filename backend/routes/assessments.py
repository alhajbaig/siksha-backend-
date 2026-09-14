"""
SIKSHA SAATHI — DIAGNOSTIC ASSESSMENTS API ROUTER
REST endpoints for:
- Standardized and Adaptive Diagnostic Test Catalog
- Dynamic Exam Simulation Session Creation (KaTeX equations, zero question leaks)
- Real-time Assessment Submission, Scoring & Gaussian Percentile Computation
- Persistent Diagnostic Scorecards & Historical Analysis
"""

import logging
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from backend.db import get_user_from_session, get_user_by_id, get_user_by_email
from backend.services.assessment_service import assessment_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/assessments", tags=["Diagnostic Assessments"])


def _resolve_user(
    authorization: Optional[str] = None,
    x_user_id: Optional[str] = None,
    x_auth_token: Optional[str] = None
) -> dict:
    """Resolves authenticated student profile from Bearer or custom headers."""
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


class AssessmentSubmitRequest(BaseModel):
    session_id: str
    answers: Dict[str, Any]  # question_id -> selected_option_int or None
    time_spent_seconds: Optional[int] = 0


@router.get("/catalog")
async def get_assessment_catalog(
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """Returns the full catalog of diagnostic tests and mock exams with user progress."""
    user = _resolve_user(authorization, x_user_id, x_auth_token)
    try:
        catalog_data = await assessment_service.get_catalog(user["id"])
        return {
            "status": "success",
            "data": catalog_data
        }
    except Exception as e:
        logger.error(f"Failed to fetch assessment catalog: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{assessment_id}/start")
async def start_assessment(
    assessment_id: str,
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """
    Launches a dynamic assessment session.
    Generates fresh, non-repetitive topic questions and returns sanitized test payload.
    """
    user = _resolve_user(authorization, x_user_id, x_auth_token)
    try:
        session_data = await assessment_service.start_assessment(assessment_id, user["id"])
        return {
            "status": "success",
            "data": session_data
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to start assessment session '{assessment_id}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{assessment_id}/submit")
async def submit_assessment(
    assessment_id: str,
    payload: AssessmentSubmitRequest,
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """
    Submits student answers, evaluates accuracy, calculates authentic Gaussian percentile,
    updates Learning Genome and Smart Revision queues, and returns diagnostic scorecard.
    """
    user = _resolve_user(authorization, x_user_id, x_auth_token)
    try:
        scorecard = await assessment_service.submit_assessment(
            assessment_id=assessment_id,
            session_id=payload.session_id,
            answers=payload.answers,
            time_spent_seconds=payload.time_spent_seconds or 0,
            user_id=user["id"]
        )
        return {
            "status": "success",
            "data": scorecard
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to evaluate assessment submission '{assessment_id}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def get_assessment_history(
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """Retrieves previous assessment attempts and score records for current student."""
    user = _resolve_user(authorization, x_user_id, x_auth_token)
    try:
        history = await assessment_service.get_history(user["id"])
        return {
            "status": "success",
            "data": history
        }
    except Exception as e:
        logger.error(f"Failed to fetch assessment history: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/attempt/{attempt_id}")
async def get_attempt_detail(
    attempt_id: str,
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """Retrieves full solutions and diagnostic scorecard for a specific past attempt."""
    user = _resolve_user(authorization, x_user_id, x_auth_token)
    try:
        detail = await assessment_service.get_attempt_detail(attempt_id, user["id"])
        if not detail:
            raise HTTPException(status_code=404, detail="Assessment attempt not found.")
        return {
            "status": "success",
            "data": detail
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch attempt detail: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
