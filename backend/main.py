"""
SIKSHA SAATHI — Main Application Entry Point
FastAPI Application serving REST APIs & Frontend Web Assets
"""

import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse

from backend.config import settings
from backend.routes import auth, rag, mentor, student, notes, practice, roadmap, revision, assessments, emergency, teacher

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-warm Supabase PostgreSQL pool on startup to eliminate first-query cold start delay
    try:
        from backend.services.supabase_service import init_pg_pool, is_supabase_configured
        if is_supabase_configured():
            init_pg_pool()
    except Exception:
        pass
    yield

# Initialize FastAPI Application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="SikshaSaathi AI Engine — Socratic Dialogue, RAG Knowledge Pipeline, and Concept Telemetry.",
    lifespan=lifespan
)

# Configure Cross-Origin Resource Sharing (CORS) for decoupled deployments
cors_origins = list(settings.CORS_ORIGINS)
if settings.FRONTEND_URL and settings.FRONTEND_URL not in cors_origins:
    cors_origins.append(settings.FRONTEND_URL.rstrip("/"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_origin_regex=r"https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(auth.router)
app.include_router(teacher.router)
app.include_router(rag.router)
app.include_router(mentor.router)
app.include_router(student.router)
app.include_router(notes.router)
app.include_router(practice.router)
app.include_router(roadmap.router)
app.include_router(revision.router)
app.include_router(assessments.router)
app.include_router(emergency.router)

# Health Check Endpoint
@app.get("/api/health", tags=["System"])
@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "online",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }

# Supabase Production Config & Status Endpoint
@app.get("/api/supabase/config", tags=["System"])
async def get_supabase_config():
    from backend.services.supabase_service import is_supabase_configured
    return {
        "status": "success",
        "is_configured": is_supabase_configured(),
        "supabase_url": settings.SUPABASE_URL,
        "supabase_anon_key": settings.SUPABASE_ANON_KEY
    }


def _find_dir(name: str) -> str:
    candidates = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", name)),
        os.path.abspath(os.path.join(os.getcwd(), name)),
        os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), name)),
    ]
    for c in candidates:
        if os.path.exists(c) and os.path.isdir(c):
            return c
    return candidates[0]

# Mount Teacher Dashboard Static Directory if exists
teacher_path = _find_dir("teacher_dashboard")
if os.path.exists(teacher_path):
    @app.get("/teacher", include_in_schema=False)
    async def redirect_teacher():
        return RedirectResponse(url="/teacher/")

    app.mount("/teacher", StaticFiles(directory=teacher_path, html=True), name="teacher_dashboard")
    app.mount("/teacher_dashboard", StaticFiles(directory=teacher_path, html=True), name="teacher_dashboard_alias")

# Mount Frontend Static Directory if directory exists
frontend_path = _find_dir("frontend")
if os.path.exists(frontend_path):
    app.mount("/frontend", StaticFiles(directory=frontend_path, html=True), name="frontend_alias")
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=settings.HOST, port=settings.PORT, reload=True)
