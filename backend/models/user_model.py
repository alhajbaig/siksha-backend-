"""
SIKHSAATHI — User Models & Schemas
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserRole(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str
    role: Optional[UserRole] = None

class UserSignUpRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.STUDENT
    
    # Student specific
    class_grade: Optional[str] = "Class 12"
    target_goal: Optional[str] = "JEE / NEET"
    
    # Teacher specific
    institution: Optional[str] = None
    subject: Optional[str] = None

class UserProfileUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    class_grade: Optional[str] = None
    target_goal: Optional[str] = None
    bio: Optional[str] = None
    institution: Optional[str] = None
    subject: Optional[str] = None
    avatar_url: Optional[str] = None

class UserProfileResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    role: UserRole
    class_grade: Optional[str] = None
    target_goal: Optional[str] = None
    bio: Optional[str] = None
    institution: Optional[str] = None
    subject: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: str
    updated_at: Optional[str] = None
    is_demo: bool = False

class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserProfileResponse
    message: str = "Authentication successful"
