"""
SIKSHA SAATHI — Backend Configuration Module
"""

import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

# Load .env from backend and workspace root
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent

load_dotenv(ROOT_DIR / ".env")
load_dotenv(BASE_DIR / ".env")

class Settings(BaseModel):
    APP_NAME: str = "SikshaSaathi API"
    APP_VERSION: str = "2.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Server configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    
    # CORS Configuration
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "")
    CORS_ORIGINS: list[str] = [
        orig.strip() for orig in os.getenv("CORS_ORIGINS", "http://localhost:8080,http://localhost:8000,http://localhost:3000,http://127.0.0.1:8080,http://127.0.0.1:8000").split(",") if orig.strip()
    ]
    
    # Security
    JWT_SECRET: str = os.getenv("JWT_SECRET", "siksha-saathi-ultra-secret-dev-key-2026")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # AI / Groq API Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_CHATBOT_API_KEY: str = os.getenv("GROQ_CHATBOT_API_KEY", os.getenv("GROQ_API_KEY", ""))
    GROQ_ROADMAP_API_KEY: str = os.getenv("GROQ_ROADMAP_API_KEY", os.getenv("GROQ_API_KEY", ""))
    GROQ_TEXT_MODEL: str = os.getenv("GROQ_TEXT_MODEL", "openai/gpt-oss-120b")
    GROQ_FALLBACK_MODELS: list[str] = ["qwen/qwen3.8-27b", "openai/gpt-oss-20b", "groq/compound-mini", "allam-2-7b"]
    GROQ_VISION_MODEL: str = "llama-3.2-11b-vision-preview"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    DEFAULT_CHUNK_SIZE: int = 512
    DEFAULT_CHUNK_OVERLAP: int = 50

    # Supabase Production Cloud Configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    SUPABASE_DB_URL: str = os.getenv("SUPABASE_DB_URL", "")
    SUPABASE_DB_HOST: str = os.getenv("SUPABASE_DB_HOST", "aws-0-ap-northeast-2.pooler.supabase.com")
    SUPABASE_DB_PORT: int = int(os.getenv("SUPABASE_DB_PORT", 5432))
    SUPABASE_DB_USER: str = os.getenv("SUPABASE_DB_USER", "postgres.hmxbwitnmrjbtrozkvul")
    SUPABASE_DB_PASSWORD: str = os.getenv("SUPABASE_DB_PASSWORD", "")
    SUPABASE_DB_NAME: str = os.getenv("SUPABASE_DB_NAME", "postgres")

settings = Settings()

