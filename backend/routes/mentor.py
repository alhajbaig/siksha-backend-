"""
SIKSHASATHI — Production AI Mentor API Routes
Full authenticated CRUD for conversations, chat, preferences, and suggestions.
"""

from typing import Optional, List
from pydantic import BaseModel
from fastapi import APIRouter, Request, HTTPException
from backend.db import (
    get_user_from_session,
    create_mentor_conversation, get_mentor_conversations,
    get_mentor_conversation, get_mentor_messages,
    delete_mentor_conversation, update_conversation_meta,
    get_ai_preferences, update_ai_preferences
)
from backend.services.mentor_service import mentor_service

router = APIRouter(prefix="/api/mentor", tags=["AI Mentor"])


# =========================================================================
# AUTH HELPER
# =========================================================================
def _get_user(request: Request) -> dict:
    token = request.headers.get("authorization", "").replace("Bearer ", "").strip()
    if not token:
        token = request.headers.get("x-auth-token", "").strip()
    x_user_id = request.headers.get("x-user-id", "").strip()

    if token == "token_demo_sandbox_session" or (not token and x_user_id == "usr_demo_sandbox"):
        return {
            "id": "usr_demo_sandbox",
            "full_name": "Guest Learner (Demo)",
            "email": "demo@sikshasaathi.sandbox",
            "role": "student",
            "class_grade": "Class 12 • Science (Demo Sandbox)",
            "target_goal": "Platform Exploration",
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

    if not token:
        raise HTTPException(status_code=401, detail="Authentication required")
    user = get_user_from_session(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid session")
    return user


# =========================================================================
# REQUEST/RESPONSE MODELS
# =========================================================================
class CreateConversationRequest(BaseModel):
    title: str = "New Conversation"
    mode: str = "socratic"
    subject: str = ""

class ChatRequest(BaseModel):
    conversation_id: str
    message: str
    mode: str = "socratic"
    chapter_id: Optional[str] = None
    attachment_base64: Optional[str] = None
    attachment_name: Optional[str] = None
    attachment_type: Optional[str] = None

class UpdatePreferencesRequest(BaseModel):
    persona: Optional[str] = None
    daily_study_minutes: Optional[int] = None
    preferred_language: Optional[str] = None

class UpdateConversationRequest(BaseModel):
    title: Optional[str] = None
    mode: Optional[str] = None
    subject: Optional[str] = None


# =========================================================================
# CONVERSATION ENDPOINTS
# =========================================================================

@router.get("/conversations")
async def list_conversations(request: Request, search: str = "", limit: int = 30):
    """Lists all mentor conversations for the authenticated user."""
    user = _get_user(request)
    convos = get_mentor_conversations(user["id"], limit=limit, search_query=search)
    return {"status": "success", "conversations": convos}


@router.post("/conversations")
async def create_conversation(request: Request, payload: CreateConversationRequest):
    """Creates a new mentor conversation."""
    user = _get_user(request)
    prefs = get_ai_preferences(user["id"])
    conv_id = create_mentor_conversation(
        user_id=user["id"],
        title=payload.title,
        mode=payload.mode,
        subject=payload.subject,
        persona=prefs.get("persona", "balanced")
    )
    return {"status": "success", "conversation_id": conv_id}


@router.get("/conversations/{conv_id}")
async def get_conversation(request: Request, conv_id: str):
    """Gets a conversation with its messages."""
    user = _get_user(request)
    conv = get_mentor_conversation(conv_id, user["id"])
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    messages = get_mentor_messages(conv_id, limit=50)
    return {"status": "success", "conversation": conv, "messages": messages}


@router.patch("/conversations/{conv_id}")
async def update_conversation(request: Request, conv_id: str, payload: UpdateConversationRequest):
    """Updates conversation metadata (title, mode, subject)."""
    user = _get_user(request)
    conv = get_mentor_conversation(conv_id, user["id"])
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    update_conversation_meta(conv_id, title=payload.title, mode=payload.mode, subject=payload.subject)
    return {"status": "success"}


@router.delete("/conversations/{conv_id}")
async def delete_conversation(request: Request, conv_id: str):
    """Deletes a conversation."""
    user = _get_user(request)
    deleted = delete_mentor_conversation(conv_id, user["id"])
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"status": "success"}


# =========================================================================
# CHAT ENDPOINT — The core AI interaction
# =========================================================================

@router.post("/chat")
async def chat(request: Request, payload: ChatRequest):
    """Sends a message and gets an AI mentor response."""
    user = _get_user(request)

    # Verify conversation ownership
    conv = get_mentor_conversation(payload.conversation_id, user["id"])
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Get user preferences for persona
    prefs = get_ai_preferences(user["id"])
    persona = prefs.get("persona", "balanced")

    # Update conversation mode if changed
    if payload.mode and payload.mode != conv.get("mode"):
        update_conversation_meta(payload.conversation_id, mode=payload.mode)

    # Process through mentor service with multimodal support
    result = await mentor_service.process_chat(
        user_id=user["id"],
        conversation_id=payload.conversation_id,
        message=payload.message,
        mode=payload.mode,
        persona=persona,
        chapter_id=payload.chapter_id,
        attachment_base64=payload.attachment_base64,
        attachment_name=payload.attachment_name,
        attachment_type=payload.attachment_type
    )

    if result.get("status") == "rate_limited":
        raise HTTPException(status_code=429, detail=result["reply"])

    return result


# =========================================================================
# PREFERENCES ENDPOINTS
# =========================================================================

@router.get("/preferences")
async def get_preferences(request: Request):
    """Gets the user's AI mentor preferences."""
    user = _get_user(request)
    prefs = get_ai_preferences(user["id"])
    return {"status": "success", "preferences": prefs}


@router.put("/preferences")
async def set_preferences(request: Request, payload: UpdatePreferencesRequest):
    """Updates the user's AI mentor preferences."""
    user = _get_user(request)
    updated = update_ai_preferences(
        user_id=user["id"],
        persona=payload.persona,
        daily_study_minutes=payload.daily_study_minutes,
        preferred_language=payload.preferred_language
    )
    return {"status": "success", "preferences": updated}


# =========================================================================
# SUGGESTIONS ENDPOINT
# =========================================================================

@router.post("/suggestions")
async def get_suggestions(request: Request, mode: str = "socratic", subject: str = ""):
    """Returns contextual quick-action suggestions based on current mode."""
    _get_user(request)
    suggestions = mentor_service.generate_suggestions(mode, subject=subject)
    return {"status": "success", "suggestions": suggestions}
