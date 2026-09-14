"""
SIKHSAATHI — RAG Knowledge Base API Routes
Supports persistent CRUD, document upload, semantic vector search, and grounded Q&A.
"""

import os
import shutil
from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Header, Query, status
from backend.models.note_model import (
    RAGQueryRequest, RAGQueryResponse, NoteDetail, NotesListResponse, UploadNoteResponse
)
from backend.services.rag_service import rag_service
from backend.db import STORAGE_DIR, get_user_from_session, get_user_by_email

router = APIRouter(prefix="/api/rag", tags=["RAG Knowledge Engine"])

def get_current_user_id(
    authorization: Optional[str] = None,
    x_user_id: Optional[str] = None,
    x_auth_token: Optional[str] = None
) -> str:
    """Extracts user identity from session token or custom header with fallback to seeded student."""
    token = None
    if isinstance(x_auth_token, str) and x_auth_token.strip():
        token = x_auth_token.strip()
    elif isinstance(authorization, str) and "Bearer " in authorization:
        token = authorization.replace("Bearer ", "").strip()

    if token == "token_demo_sandbox_session" or (not token and x_user_id == "usr_demo_sandbox"):
        return "usr_demo_sandbox"

    if token and token.startswith("ey") and token.count(".") == 2:
        try:
            from backend.services.supabase_service import verify_supabase_token, is_supabase_configured
            if is_supabase_configured():
                u = verify_supabase_token(token)
                if u:
                    return str(u["id"])
        except Exception:
            pass

    if token:
        user = get_user_from_session(token)
        if user:
            return user["id"]

    raise HTTPException(
        status_code=401,
        detail="Active authentication session required."
    )

@router.get("/notes", response_model=NotesListResponse)
async def get_all_notes(
    subject: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None)
):
    """
    Retrieve all notes for authenticated user with dynamic subject counts.
    """
    user_id = get_current_user_id(authorization, x_user_id)
    return rag_service.get_all_notes(user_id=user_id, subject_filter=subject, search=search)

@router.get("/notes/{note_id}", response_model=NoteDetail)
async def get_note(
    note_id: str,
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None)
):
    """
    Retrieve note content and indexed semantic chunks for active note reader.
    """
    user_id = get_current_user_id(authorization, x_user_id)
    note = rag_service.get_note_by_id(note_id, user_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.post("/query", response_model=RAGQueryResponse)
async def query_rag(
    payload: RAGQueryRequest,
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None)
):
    """
    Perform semantic vector query across indexed note chunks with grounded citation.
    """
    user_id = get_current_user_id(authorization, x_user_id)
    return await rag_service.process_query(
        user_id=user_id,
        note_id=payload.note_id,
        query=payload.query,
        query_type=payload.query_type or "custom"
    )

@router.post("/upload", response_model=UploadNoteResponse)
async def upload_document(
    title: str = Form(...),
    subject: str = Form("phys"),
    text_content: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None)
):
    """
    Upload and parse PDF / Scan / Notes through 4-stage ingestion pipeline.
    """
    user_id = get_current_user_id(authorization, x_user_id)
    saved_file_path = None
    file_type = "txt"

    if file and file.filename:
        ext = os.path.splitext(file.filename)[1].lower().replace(".", "")
        file_type = ext or "txt"
        user_upload_dir = os.path.join(STORAGE_DIR, user_id)
        os.makedirs(user_upload_dir, exist_ok=True)
        safe_filename = f"{int(os.times().elapsed * 1000)}_{file.filename}"
        saved_file_path = os.path.join(user_upload_dir, safe_filename)

        with open(saved_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    note_detail = rag_service.ingest_note(
        user_id=user_id,
        title=title,
        subject=subject,
        file_path=saved_file_path,
        file_type=file_type,
        text_content=text_content
    )

    return UploadNoteResponse(
        status="indexed",
        note=note_detail,
        message=f"Successfully vectorized and indexed '{title}' into RAG knowledge store."
    )

@router.delete("/notes/{note_id}")
async def delete_note(
    note_id: str,
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None)
):
    """
    Delete note, its semantic chunks, embeddings, and stored file.
    """
    user_id = get_current_user_id(authorization, x_user_id)
    success = rag_service.delete_note(note_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"status": "success", "message": "Note deleted successfully"}

@router.post("/notes/{note_id}/reindex", response_model=NoteDetail)
async def reindex_note(
    note_id: str,
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None)
):
    """
    Regenerate semantic chunks and vector embeddings for an existing note.
    """
    user_id = get_current_user_id(authorization, x_user_id)
    note = rag_service.reindex_note(note_id, user_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note
