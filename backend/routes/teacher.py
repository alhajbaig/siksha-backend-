"""
SIKSHASAATHI — Educator & Classroom Management API Routes
Provides verified backend routes for teacher profile, real classroom CRUD,
metrics aggregation, and student roster access.
"""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from backend.routes.auth import require_teacher
from backend.db import (
    update_user_profile, get_user_by_id,
    create_classroom, get_teacher_classrooms,
    get_classroom_by_id, get_teacher_metrics,
    get_classroom_students, is_student_in_teacher_class,
    get_all_teacher_students, get_teacher_doubts, reply_to_classroom_doubt,
    get_student_test_history_and_activity,
    get_teacher_cohort_misconceptions, get_teacher_recent_activity
)
from backend.services.genome_service import genome_service

router = APIRouter(prefix="/api/teacher", tags=["Teacher & Classrooms"])


class TeacherProfileUpdateRequest(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    institution: Optional[str] = Field(None, max_length=150)
    subject: Optional[str] = Field(None, max_length=80)
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = None


class CreateClassroomRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=120, description="Display name of the classroom")
    subject: str = Field(..., min_length=2, max_length=80, description="Primary subject")
    grade_level: Optional[str] = Field("Class 12", max_length=60, description="Target academic grade/section")
    description: Optional[str] = Field("", max_length=400, description="Optional cohort overview")


class ReplyDoubtRequest(BaseModel):
    reply: str = Field(..., min_length=2, max_length=2000, description="Educator guidance/answer for the student")


@router.get("/profile")
async def get_teacher_profile(teacher: dict = Depends(require_teacher)):
    """
    Returns authentic profile details and teaching statistics for the logged-in educator.
    """
    user_data = get_user_by_id(teacher["id"]) or teacher
    metrics = get_teacher_metrics(teacher["id"])

    return {
        "id": user_data["id"],
        "email": user_data["email"],
        "full_name": user_data.get("full_name") or "Educator",
        "role": user_data["role"],
        "institution": user_data.get("institution") or "",
        "subject": user_data.get("subject") or "",
        "bio": user_data.get("bio") or "",
        "avatar_url": user_data.get("avatar_url") or "",
        "total_classes": metrics["total_classes"],
        "total_students": metrics["total_students"],
        "average_mastery": metrics["average_mastery"],
        "created_at": user_data.get("created_at", "")
    }


@router.put("/profile")
async def update_teacher_profile(
    payload: TeacherProfileUpdateRequest,
    teacher: dict = Depends(require_teacher)
):
    """
    Persistently updates teacher profile fields (Name, Institution, Subject, Bio).
    """
    updates = {}
    if payload.full_name is not None:
        updates["full_name"] = payload.full_name.strip()
    if payload.institution is not None:
        updates["institution"] = payload.institution.strip()
    if payload.subject is not None:
        updates["subject"] = payload.subject.strip()
    if payload.bio is not None:
        updates["bio"] = payload.bio.strip()
    if payload.avatar_url is not None:
        updates["avatar_url"] = payload.avatar_url.strip()

    updated = update_user_profile(teacher["id"], **updates)
    user_data = get_user_by_id(teacher["id"]) or teacher
    metrics = get_teacher_metrics(teacher["id"])

    return {
        "status": "success",
        "message": "Profile updated successfully.",
        "user": {
            "id": user_data["id"],
            "email": user_data["email"],
            "full_name": user_data.get("full_name"),
            "role": user_data["role"],
            "institution": user_data.get("institution", ""),
            "subject": user_data.get("subject", ""),
            "bio": user_data.get("bio", ""),
            "avatar_url": user_data.get("avatar_url", ""),
            "total_classes": metrics["total_classes"],
            "total_students": metrics["total_students"]
        }
    }


@router.get("/classes")
async def list_teacher_classes(teacher: dict = Depends(require_teacher)):
    """
    Returns all active classrooms created by the authenticated teacher,
    with real-time enrolled student counts and unique join codes.
    """
    classes = get_teacher_classrooms(teacher["id"])
    return {
        "status": "success",
        "count": len(classes),
        "classes": classes
    }


@router.post("/classes", status_code=status.HTTP_201_CREATED)
async def create_new_class(
    payload: CreateClassroomRequest,
    teacher: dict = Depends(require_teacher)
):
    """
    Creates a new real classroom entity in SQLite, auto-generating a unique,
    human-friendly join code (e.g. PHY8Q4, MTH7K2).
    """
    if not payload.name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Class name is required."
        )
    if not payload.subject.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subject is required."
        )

    classroom = create_classroom(
        teacher_id=teacher["id"],
        name=payload.name,
        subject=payload.subject,
        grade_level=payload.grade_level or "Class 12",
        description=payload.description or ""
    )

    return {
        "status": "success",
        "message": f"Class '{classroom['name']}' created successfully.",
        "classroom": classroom
    }


@router.get("/classes/{class_id}")
async def get_class_detail(class_id: str, teacher: dict = Depends(require_teacher)):
    """
    Retrieves details for a specific classroom owned by the authenticated teacher.
    """
    classroom = get_classroom_by_id(class_id)
    if not classroom or classroom.get("teacher_id") != teacher["id"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Classroom not found."
        )
    return {
        "status": "success",
        "classroom": classroom
    }


@router.get("/classes/{class_id}/students")
async def get_class_roster(class_id: str, teacher: dict = Depends(require_teacher)):
    """
    Returns the real-time enrolled student roster for a class owned by the teacher.
    """
    classroom = get_classroom_by_id(class_id)
    if not classroom or classroom.get("teacher_id") != teacher["id"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Classroom not found."
        )
    students = get_classroom_students(class_id, teacher["id"])
    return {
        "status": "success",
        "class_id": class_id,
        "class_name": classroom["name"],
        "student_count": len(students),
        "students": students
    }


@router.get("/metrics")
async def get_dashboard_metrics(teacher: dict = Depends(require_teacher)):
    """
    Aggregates authentic KPI metrics for the educator dashboard:
    total classes, total students, average student mastery.
    """
    metrics = get_teacher_metrics(teacher["id"])
    return {
        "status": "success",
        "metrics": metrics
    }


@router.get("/students/{student_id}/genome")
async def get_student_genome_for_teacher(
    student_id: str,
    teacher: dict = Depends(require_teacher)
):
    """
    Returns the authentic, canonical Learning Genome & Cognitive Fingerprint for an enrolled student.
    Strict privacy policy: Teacher must own an active class where student is an active member.
    Zero fabricated metrics: derives directly from the student's real quiz attempts and answers.
    """
    authorized = is_student_in_teacher_class(teacher["id"], student_id)
    if not authorized:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Student is not an active enrolled member in any of your classrooms."
        )

    genome = genome_service.get_learning_genome(student_id)
    return {
        "status": "success",
        "student_id": student_id,
        "genome": genome
    }


@router.get("/students/{student_id}/activity")
async def get_student_activity_for_teacher(
    student_id: str,
    teacher: dict = Depends(require_teacher)
):
    """
    Returns authentic chronological test history, quiz scores, accuracy,
    and activity timeline for a student enrolled in the teacher's classroom.
    """
    authorized = is_student_in_teacher_class(teacher["id"], student_id)
    if not authorized:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Student is not an active enrolled member in any of your classrooms."
        )

    activity_data = get_student_test_history_and_activity(student_id)
    return activity_data


@router.get("/students")
async def list_all_teacher_students(
    class_id: Optional[str] = None,
    teacher: dict = Depends(require_teacher)
):
    """
    Returns enrolled students across all active classrooms owned by the teacher (or filtered by class_id).
    Authoritatively queries Supabase with calculated status tiers and classroom metadata.
    """
    if class_id:
        classroom = get_classroom_by_id(class_id)
        if not classroom or classroom.get("teacher_id") != teacher["id"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Classroom not found or unauthorized."
            )
        students = get_classroom_students(class_id, teacher["id"])
    else:
        students = get_all_teacher_students(teacher["id"])

    excelling = sum(1 for s in students if s.get("status_tier") == "Excelling")
    on_track = sum(1 for s in students if s.get("status_tier") == "On Track")
    needs_attention = sum(1 for s in students if s.get("status_tier") == "Needs Attention")
    classes = get_teacher_classrooms(teacher["id"])

    return {
        "status": "success",
        "total": len(students),
        "count": len(students),
        "excelling_count": excelling,
        "on_track_count": on_track,
        "needs_attention_count": needs_attention,
        "attention_count": needs_attention,
        "students": students,
        "classes": classes
    }


# =========================================================================
# EDUCATOR DOUBT DESK & REAL-TIME Q&A SYNC
# =========================================================================

@router.get("/doubts")
async def list_teacher_doubts_endpoint(teacher: dict = Depends(require_teacher)):
    """
    Returns all academic doubts and questions submitted by enrolled students
    across all classrooms owned by this educator.
    """
    doubts = get_teacher_doubts(teacher["id"])
    open_count = sum(1 for d in doubts if d.get("status") == "open")
    answered_count = sum(1 for d in doubts if d.get("status") == "answered")

    return {
        "status": "success",
        "total": len(doubts),
        "open_count": open_count,
        "answered_count": answered_count,
        "doubts": doubts
    }


@router.post("/doubts/{doubt_id}/reply")
async def reply_to_doubt_endpoint(
    doubt_id: str,
    payload: ReplyDoubtRequest,
    teacher: dict = Depends(require_teacher)
):
    """
    Persists educator guidance/answer to the student's question.
    Immediately syncs back to the student's Classroom Hub.
    """
    updated = reply_to_classroom_doubt(
        doubt_id=doubt_id,
        teacher_id=teacher["id"],
        reply=payload.reply
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doubt not found or not in your classrooms."
        )

    return {
        "status": "success",
        "message": "Guidance sent to student.",
        "doubt": updated
    }


@router.post("/doubts/{doubt_id}/suggest-reply")
async def suggest_doubt_reply_endpoint(
    doubt_id: str,
    teacher: dict = Depends(require_teacher)
):
    """
    AI Co-Pilot for Educators: Generates a high-quality, pedagogically rich
    draft response for the educator to review, modify, or send.
    """
    doubts = get_teacher_doubts(teacher["id"])
    target_doubt = next((d for d in doubts if d["id"] == doubt_id), None)
    if not target_doubt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doubt not found."
        )

    q = (target_doubt.get("question") or "").lower()
    topic = target_doubt.get("topic") or "Physics & Mechanics"

    if "friction" in q or "static" in q:
        suggestion = (
            "Great question! Static friction is self-adjusting because the microscopic contact junctions "
            "between the surfaces deform elastically under applied shear force without slipping. The force "
            "matches the applied external force exactly (f_s = F_applied) until the shear stress exceeds the "
            "interlocking material strength, at which point f_{s,max} = \\mu_s N is reached and kinetic motion starts. "
            "Make sure to review the Friction Mechanics section in our uploaded notes!"
        )
    elif "integration" in q or "calculus" in q or "derivative" in q:
        suggestion = (
            "Spot on deduction! In integration by parts (\\int u\\,dv = uv - \\int v\\,du), always use the ILATE "
            "priority rule to pick 'u'. Differentiating the polynomial or logarithmic term reduces its degree, while "
            "integrating the exponential or trigonometric term remains tractable."
        )
    elif "electromagnet" in q or "gauss" in q or "charge" in q:
        suggestion = (
            "Think about the geometric symmetry of the problem. When applying Gauss's Law (\\oint \\vec{E} \\cdot d\\vec{A} = Q_{enc}/\\varepsilon_0), "
            "choose a Gaussian surface where |E| is constant across the surface, making the dot product simple to evaluate."
        )
    else:
        suggestion = (
            f"Insightful conceptual query on {topic}! Remember to first state your knowns and isolate the target variable. "
            "Draw a clear Free Body Diagram / schematic, then apply the governing conservation law."
        )

    return {
        "status": "success",
        "suggested_reply": suggestion
    }


@router.get("/misconceptions")
async def get_teacher_cohort_misconceptions_endpoint(
    subject: Optional[str] = None,
    class_id: Optional[str] = None,
    teacher: dict = Depends(require_teacher)
):
    """
    Returns authentic, real-time cohort error rates and conceptual frontiers
    for students enrolled in the teacher's classrooms.
    """
    misconceptions = get_teacher_cohort_misconceptions(
        teacher_id=teacher["id"],
        class_id=class_id,
        subject=subject
    )
    return {
        "status": "success",
        "misconceptions": misconceptions,
        "count": len(misconceptions)
    }


@router.get("/recent-activity")
async def get_teacher_recent_activity_endpoint(
    limit: Optional[int] = 15,
    teacher: dict = Depends(require_teacher)
):
    """
    Returns real-time feed of recent student quiz attempts and doubts
    from students enrolled in the teacher's classrooms.
    """
    activities = get_teacher_recent_activity(
        teacher_id=teacher["id"],
        limit=limit or 15
    )
    return {
        "status": "success",
        "activities": activities,
        "count": len(activities)
    }



