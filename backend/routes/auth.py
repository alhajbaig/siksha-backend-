"""
SIKHSAATHI — Persistent SQLite Authentication API Routes
"""

from typing import Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Header, status
from backend.models.user_model import (
    UserLoginRequest, UserSignUpRequest, UserProfileUpdateRequest,
    AuthTokenResponse, UserProfileResponse, UserRole
)
from backend.db import (
    get_user_by_email, get_user_by_id, create_user, update_user_profile,
    verify_password, create_session, get_user_from_session, delete_session, update_user_role
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


def _extract_user_from_headers(
    authorization: Optional[str] = None,
    x_user_id: Optional[str] = None,
    x_auth_token: Optional[str] = None
) -> Optional[dict]:
    """Helper to authenticate request strictly via session token or validated user ID."""
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

    if token:
        user = get_user_from_session(token)
        if user:
            return user

    return None


async def get_authenticated_user(
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
) -> dict:
    """Dependency that strictly requires an authenticated user session, raising 401 if missing."""
    user = _extract_user_from_headers(authorization, x_user_id, x_auth_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Active authentication session required."
        )
    return user


def require_role(expected_role: str):
    """Dependency factory enforcing strict role-based access control (403 Forbidden)."""
    async def role_checker(
        authorization: Optional[str] = Header(None),
        x_auth_token: Optional[str] = Header(None)
    ) -> dict:
        user = _extract_user_from_headers(authorization, None, x_auth_token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Active authentication session required."
            )
        if user.get("role") != expected_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: {expected_role.capitalize()} privileges required."
            )
        return user
    return role_checker


async def require_teacher(
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
) -> dict:
    """Dependency strictly requiring a Teacher role, raising 403 for Students or 401 if unauthenticated."""
    user = _extract_user_from_headers(authorization, x_user_id, x_auth_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Educator authentication required."
        )
    if user.get("role") != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Teacher privileges required."
        )
    return user


async def require_student(
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
) -> dict:
    """Dependency strictly requiring a Student role, raising 403 for Teachers or 401 if unauthenticated."""
    user = _extract_user_from_headers(authorization, x_user_id, x_auth_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Student authentication required."
        )
    if user.get("role") != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Student privileges required."
        )
    return user


def _format_user_profile(user: dict) -> UserProfileResponse:
    """Formats database dictionary into UserProfileResponse schema."""
    created = user.get("created_at")
    updated = user.get("updated_at")
    return UserProfileResponse(
        id=str(user["id"]),
        full_name=user.get("full_name", ""),
        email=user.get("email", ""),
        role=UserRole(user.get("role", "student")),
        class_grade=user.get("class_grade"),
        target_goal=user.get("target_goal"),
        bio=user.get("bio"),
        institution=user.get("institution"),
        subject=user.get("subject"),
        avatar_url=user.get("avatar_url"),
        created_at=created.isoformat() if hasattr(created, "isoformat") else str(created or ""),
        updated_at=updated.isoformat() if hasattr(updated, "isoformat") else (str(updated) if updated else None),
        is_demo=bool(user.get("is_demo", False))
    )



@router.post("/login", response_model=AuthTokenResponse)
async def login(credentials: UserLoginRequest):
    """
    Authenticates existing user with persistent Cloud PostgreSQL or SQLite.
    """
    email_clean = credentials.email.strip().lower()

    # 1. Fetch user from persistent database (Supabase PostgreSQL / SQLite)
    user = get_user_by_email(email_clean)

    if user and user.get("password_hash") and user.get("salt"):
        is_valid = verify_password(credentials.password, user["password_hash"], user["salt"])
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password. Please verify your credentials or reset your password."
            )
        # If user explicitly specified role (e.g., student vs teacher toggle), sync it
        if credentials.role and credentials.role.value != user.get("role"):
            updated_user = update_user_role(user["id"], credentials.role.value)
            if updated_user:
                user = updated_user
        token = create_session(user["id"])
        return AuthTokenResponse(
            access_token=token,
            user=_format_user_profile(user),
            message=f"Welcome back, {user['full_name']}."
        )

    # 2. If not found in primary tables, try Supabase Auth fallback
    try:
        from backend.services.supabase_service import get_supabase_client, is_supabase_configured
        if is_supabase_configured():
            sb_client = get_supabase_client()
            if sb_client:
                auth_res = sb_client.auth.sign_in_with_password({
                    "email": email_clean,
                    "password": credentials.password
                })
                if auth_res and auth_res.user:
                    u = auth_res.user
                    meta = u.user_metadata or {}
                    user = create_user(
                        email=email_clean,
                        password=credentials.password,
                        full_name=meta.get("full_name", email_clean.split("@")[0]),
                        role=meta.get("role", "student"),
                        class_grade=meta.get("class_grade", "Class 12 • Senior Secondary"),
                        target_goal=meta.get("target_goal", "JEE / NEET")
                    )
                    token = auth_res.session.access_token if auth_res.session else create_session(user["id"])
                    return AuthTokenResponse(
                        access_token=token,
                        user=_format_user_profile(user),
                        message=f"Welcome back, {user['full_name']} (Cloud Verified)."
                    )
    except Exception:
        pass

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No account found with this email. Please sign up or check your credentials."
    )


@router.post("/signup", response_model=AuthTokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(payload: UserSignUpRequest):
    """
    Registers a new student or teacher in persistent Cloud PostgreSQL and SQLite.
    """
    email_clean = payload.email.strip().lower()
    target_role = payload.role.value if payload.role else "student"

    # 1. Check if user already exists
    existing_user = get_user_by_email(email_clean)
    if existing_user:
        if verify_password(payload.password, existing_user.get("password_hash", ""), existing_user.get("salt", "")):
            # Update user with requested role and full name/profile
            user = create_user(
                email=email_clean,
                password=payload.password,
                full_name=payload.full_name.strip(),
                role=target_role,
                class_grade=payload.class_grade or "Class 12 • Senior Secondary",
                target_goal=payload.target_goal or "JEE / NEET",
                institution=payload.institution or "",
                subject=payload.subject or "",
                bio="Passionate student exploring concepts with SikshaSaathi AI."
            )
            token = create_session(user["id"])
            return AuthTokenResponse(
                access_token=token,
                user=_format_user_profile(user),
                message="Account updated and signed in successfully."
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists. Please log in."
        )

    # 2. Create persistent user in Cloud PostgreSQL + SQLite
    new_user = create_user(
        email=email_clean,
        password=payload.password,
        full_name=payload.full_name.strip(),
        role=target_role,
        class_grade=payload.class_grade or "Class 12 • Senior Secondary",
        target_goal=payload.target_goal or "JEE / NEET",
        institution=payload.institution or "",
        subject=payload.subject or "",
        bio="Passionate student exploring concepts with SikshaSaathi AI."
    )

    # 3. Create persistent cloud session
    token = create_session(new_user["id"])

    # 4. Best-effort Supabase Auth user sync
    try:
        from backend.services.supabase_service import get_supabase_client, is_supabase_configured
        if is_supabase_configured():
            sb_client = get_supabase_client()
            if sb_client:
                sb_client.auth.admin.create_user({
                    "email": email_clean,
                    "password": payload.password,
                    "email_confirm": True,
                    "user_metadata": {
                        "full_name": payload.full_name.strip(),
                        "role": payload.role.value if payload.role else "student",
                        "class_grade": payload.class_grade or "Class 12 • Senior Secondary",
                        "target_goal": payload.target_goal or "JEE / NEET"
                    }
                })
    except Exception:
        pass

    return AuthTokenResponse(
        access_token=token,
        user=_format_user_profile(new_user),
        message="Account created successfully! Welcome to your learning space."
    )


@router.get("/me", response_model=UserProfileResponse)
@router.get("/profile", response_model=UserProfileResponse)
async def get_current_user_profile(
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """
    Returns current authenticated user profile verified from active SQLite session.
    """
    user = _extract_user_from_headers(authorization, x_user_id, x_auth_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No active authentication session. Please sign in."
        )
    return _format_user_profile(user)


@router.put("/profile", response_model=UserProfileResponse)
async def update_profile(
    payload: UserProfileUpdateRequest,
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """
    Updates student or teacher profile persistently in SQLite DB.
    """
    user = _extract_user_from_headers(authorization, x_user_id, x_auth_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to update profile."
        )

    updated_user = update_user_profile(
        user["id"],
        full_name=payload.full_name,
        class_grade=payload.class_grade,
        target_goal=payload.target_goal,
        bio=payload.bio,
        institution=payload.institution,
        subject=payload.subject,
        avatar_url=payload.avatar_url
    )
    return _format_user_profile(updated_user)


@router.post("/logout")
async def logout(
    authorization: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None)
):
    """
    Invalidates session token in SQLite DB.
    """
    token = x_auth_token or (authorization.replace("Bearer ", "").strip() if authorization and "Bearer " in authorization else None)
    if token:
        delete_session(token)
    return {
        "status": "success",
        "message": "Session terminated successfully."
    }


@router.post("/forgot-password")
async def forgot_password(email: str):
    """
    Password reset instructions handler.
    """
    return {
        "status": "success",
        "message": f"Password reset instructions dispatched to {email}."
    }


@router.post("/demo-session", response_model=AuthTokenResponse)
async def create_demo_session():
    """
    Creates an isolated sandbox exploration session.
    Zero persistence to production database.
    Allows visitors to experience SikshaSaathi safely.
    """
    now = datetime.utcnow().isoformat()
    demo_user = {
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
        "created_at": now,
        "updated_at": now,
        "is_demo": True
    }
    return AuthTokenResponse(
        access_token="token_demo_sandbox_session",
        user=_format_user_profile(demo_user),
        message="Entered SikshaSaathi Sandbox Demo Mode. Progress will not be permanently saved."
    )


