"""
SIKHSAATHI — AI Personalized Roadmap API Routes
Provides secure student endpoints to retrieve, generate, and update AI learning roadmaps.
"""

from typing import Optional
from fastapi import APIRouter, Header, HTTPException

from backend.db import get_user_from_session, get_user_by_id, get_user_by_email
from backend.services.roadmap_service import roadmap_service

router = APIRouter(prefix="/api/student/roadmap", tags=["AI Personalized Roadmap"])


def _resolve_user(
    authorization: Optional[str] = None,
    x_user_id: Optional[str] = None,
    x_auth_token: Optional[str] = None
) -> dict:
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


@router.get("")
async def get_roadmap_status_endpoint(
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """
    Returns active roadmap, whether it exists, and if it is outdated due to new quiz completions.
    """
    user = _resolve_user(authorization, x_user_id, x_auth_token)
    status = roadmap_service.get_roadmap_status(user["id"])
    return {
        "status": "success",
        "user_id": user["id"],
        **status
    }


@router.post("/generate")
async def generate_roadmap_endpoint(
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """
    Generates or refreshes the AI personalized learning roadmap using Groq LLM and live database progress.
    """
    user = _resolve_user(authorization, x_user_id, x_auth_token)
    result = await roadmap_service.generate_roadmap(user["id"])
    return result
