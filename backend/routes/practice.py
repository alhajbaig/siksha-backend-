"""
SIKSHA SAATHI — Practice & Progress API Router
Provides clean, secure endpoints for Subject selection, Level unlocking, 10-Question Quizzes,
Server-side Score Calculation, and Unified Progress Engine.
"""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Header, HTTPException, Query
from pydantic import BaseModel

from backend.db import (
    get_user_from_session, get_user_by_id, get_user_by_email,
    get_practice_subjects, get_practice_subject_levels,
    get_practice_level_questions, submit_quiz_attempt,
    get_user_progress_summary, get_quiz_attempt_review,
    get_user_quiz_history
)

router = APIRouter(prefix="/api/practice", tags=["Practice Arena & Quizzes"])


def _normalize_option(opt: Any) -> int:
    if opt is None:
        return -1
    if isinstance(opt, int):
        return opt
    if isinstance(opt, str):
        mapping = {"A": 0, "B": 1, "C": 2, "D": 3}
        cleaned = opt.strip().upper()
        if cleaned in mapping:
            return mapping[cleaned]
        try:
            return int(cleaned)
        except ValueError:
            return -1
    return -1


class QuizAnswerItem(BaseModel):
    question_id: str
    selected_option: Any = -1  # 0: A, 1: B, 2: C, 3: D, or 'A'/'B'/'C'/'D'


class QuizSubmitRequest(BaseModel):
    subject_id: str
    level_number: int
    answers: List[QuizAnswerItem]
    time_spent_seconds: Optional[int] = 0


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


@router.get("/subjects")
async def list_practice_subjects(
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """
    Returns the 4 core subjects with real-time level progress (e.g. 3/5 complete) for the user.
    """
    user = _resolve_user(authorization, x_user_id, x_auth_token)
    subjects = get_practice_subjects(user["id"])
    return {
        "status": "success",
        "user_id": user["id"],
        "subjects": subjects
    }


@router.get("/subject/{subject_id}/levels")
async def list_subject_levels(
    subject_id: str,
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """
    Returns exactly 5 levels for the subject with real unlocking state (unlocked, completed, locked),
    best scores, and attempt counts.
    """
    user = _resolve_user(authorization, x_user_id, x_auth_token)
    levels = get_practice_subject_levels(subject_id.lower(), user["id"])
    if not levels:
        raise HTTPException(status_code=404, detail="Subject not found")

    return {
        "status": "success",
        "subject_id": subject_id.lower(),
        "levels": levels
    }


@router.get("/quiz/{subject_id}/{level_number}")
async def get_level_quiz(
    subject_id: str,
    level_number: int,
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """
    Retrieves the 10 questions for the selected subject and level.
    Correct answers and full explanations are hidden for quiz integrity.
    """
    user = _resolve_user(authorization, x_user_id, x_auth_token)
    if level_number < 1 or level_number > 5:
        raise HTTPException(status_code=400, detail="Level number must be between 1 and 5")

    # Verify if level is unlocked for the user
    levels = get_practice_subject_levels(subject_id.lower(), user["id"])
    lvl_info = next((l for l in levels if l["level_number"] == level_number), None)
    if not lvl_info:
        raise HTTPException(status_code=404, detail="Level not found")

    if lvl_info["status"] == "locked":
        raise HTTPException(status_code=403, detail=f"Level {level_number} is locked. Complete Level {level_number - 1} first.")

    from backend.services.question_engine import dynamic_question_engine
    try:
        questions = await dynamic_question_engine.get_level_quiz_questions(
            subject_id=subject_id.lower(),
            level_number=level_number,
            count=10,
            user_id=user["id"]
        )
    except Exception as err:
        questions = get_practice_level_questions(subject_id.lower(), level_number, sanitize=True)

    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this level")

    return {
        "status": "success",
        "subject_id": subject_id.lower(),
        "level_number": level_number,
        "level_title": lvl_info["title"],
        "total_questions": len(questions),
        "questions": questions
    }


@router.post("/quiz/submit")
async def submit_quiz(
    payload: QuizSubmitRequest,
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """
    Server-side authoritative score calculation.
    Compares answers against SQLite questions, records attempt, recalculates mastery,
    and returns score, percentage, and full explanations.
    """
    user = _resolve_user(authorization, x_user_id, x_auth_token)
    
    answers_dicts = [
        {"question_id": a.question_id, "selected_option": _normalize_option(a.selected_option)}
        for a in payload.answers
    ]
    result = submit_quiz_attempt(
        user_id=user["id"],
        subject_id=payload.subject_id.lower(),
        level_number=payload.level_number,
        answers=answers_dicts,
        time_spent_seconds=payload.time_spent_seconds or 0
    )

    return {
        "status": "success",
        "result": result
    }


@router.get("/history")
async def get_quiz_history(
    limit: Optional[int] = Query(30, ge=1, le=100),
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """
    Returns the student's chronological history of completed quiz attempts with scores and timestamps.
    """
    user = _resolve_user(authorization, x_user_id, x_auth_token)
    history = get_user_quiz_history(user["id"], limit=limit)
    return {
        "status": "success",
        "user_id": user["id"],
        "history": history
    }


@router.get("/attempt/{attempt_id}/review")
async def review_quiz_attempt(
    attempt_id: str,
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """
    Reconstructs the persistent 10-question Answer Key from SQLite for any historical attempt.
    Enforces strict user ownership.
    """
    user = _resolve_user(authorization, x_user_id, x_auth_token)
    attempt_review = get_quiz_attempt_review(user["id"], attempt_id)
    if not attempt_review:
        raise HTTPException(status_code=404, detail="Quiz attempt not found or access denied")

    return {
        "status": "success",
        "attempt": attempt_review
    }

