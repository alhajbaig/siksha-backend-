"""
SIKHSAATHI — RAG & Note Pydantic Models & Schemas
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class ChunkModel(BaseModel):
    id: int
    text: str
    score: float = 0.95
    page_number: Optional[int] = 1
    section_title: Optional[str] = ""

class NoteSummary(BaseModel):
    id: str
    title: str
    subject: str          # 'chem', 'phys', 'math', 'cs'
    badge: str            # 'CHEMISTRY', 'PHYSICS', 'MATHEMATICS', 'COMP SCIENCE'
    format: str           # 'PDF • 14 CHUNKS', 'SCAN • 10 CHUNKS', etc.
    chunk_count: int
    reading_time_min: int = 3
    word_count: int = 250
    status: str = "indexed"  # 'indexed', 'processing', 'failed'
    updated_at: str

class NoteDetail(BaseModel):
    id: str
    title: str
    subject: str
    badge: str
    format: str
    body: str
    word_count: int = 250
    reading_time_min: int = 3
    chunk_count: int = 4
    status: str = "indexed"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    chunks: List[ChunkModel] = []

class SubjectCounts(BaseModel):
    all: int = 0
    chem: int = 0
    phys: int = 0
    math: int = 0
    cs: int = 0

class NotesListResponse(BaseModel):
    status: str = "success"
    notes: List[NoteSummary]
    subject_counts: SubjectCounts
    total_indexed: int

class CitationModel(BaseModel):
    chunk_id: int
    text: str
    similarity_score: float
    page_number: int = 1
    note_title: Optional[str] = None
    grounded_confidence: str = "98% Grounded in Active Note"

class RAGQueryRequest(BaseModel):
    note_id: Optional[str] = None
    query: str
    query_type: Optional[str] = "custom"  # "summary", "formulas", "quiz", "traps", "custom"

class RAGQueryResponse(BaseModel):
    note_id: Optional[str] = None
    query: str
    answer: str
    citations: List[CitationModel]
    retrieval_time_ms: float = 38.5
    grounded: bool = True

class UploadNoteResponse(BaseModel):
    status: str
    note: NoteDetail
    message: str
