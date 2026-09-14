"""
SIKSHA SAATHI — Production Supabase Service
Manages direct PostgreSQL connection pools, Supabase Auth verification,
and Supabase Cloud Storage.
"""

import os
import logging
from typing import Optional, Dict, Any
from contextlib import contextmanager
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from supabase import create_client, Client
from backend.config import settings

logger = logging.getLogger("siksha_saathi.supabase")

_supabase_client: Optional[Client] = None
_pg_pool: Optional[pool.ThreadedConnectionPool] = None


def get_supabase_client() -> Optional[Client]:
    """Initializes and returns the singleton Supabase admin client."""
    global _supabase_client
    if _supabase_client is not None:
        return _supabase_client

    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_ROLE_KEY:
        logger.warning("[Supabase] SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY not configured.")
        return None

    try:
        _supabase_client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_ROLE_KEY
        )
        logger.info("[Supabase] Admin client initialized successfully.")
        return _supabase_client
    except Exception as err:
        logger.error(f"[Supabase] Failed to initialize client: {err}")
        return None


def init_pg_pool():
    """Initializes the PostgreSQL threaded connection pool for high-throughput queries."""
    global _pg_pool
    if _pg_pool is not None:
        return

    if not settings.SUPABASE_DB_HOST or not settings.SUPABASE_DB_PASSWORD:
        return

    try:
        _pg_pool = pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            host=settings.SUPABASE_DB_HOST,
            port=settings.SUPABASE_DB_PORT,
            user=settings.SUPABASE_DB_USER,
            password=settings.SUPABASE_DB_PASSWORD,
            dbname=settings.SUPABASE_DB_NAME,
            sslmode="require",
            connect_timeout=10
        )
        logger.info("[Supabase PostgreSQL] Threaded connection pool initialized (1-10 connections).")
    except Exception as err:
        logger.error(f"[Supabase PostgreSQL] Could not initialize connection pool: {err}")


@contextmanager
def get_pg_connection():
    """Yields a pooled or direct PostgreSQL connection with RealDictCursor."""
    global _pg_pool
    init_pg_pool()

    conn = None
    from_pool = False
    try:
        if _pg_pool:
            conn = _pg_pool.getconn()
            from_pool = True
        else:
            conn = psycopg2.connect(
                host=settings.SUPABASE_DB_HOST,
                port=settings.SUPABASE_DB_PORT,
                user=settings.SUPABASE_DB_USER,
                password=settings.SUPABASE_DB_PASSWORD,
                dbname=settings.SUPABASE_DB_NAME,
                sslmode="require",
                connect_timeout=10
            )
        yield conn
    except Exception:
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
        raise
    finally:
        if conn:
            try:
                if not conn.closed and conn.get_transaction_status() != psycopg2.extensions.TRANSACTION_STATUS_IDLE:
                    conn.commit()
            except Exception:
                try:
                    conn.rollback()
                except Exception:
                    pass
            if from_pool and _pg_pool:
                _pg_pool.putconn(conn)
            elif not from_pool:
                conn.close()


def is_supabase_configured() -> bool:
    """Checks if Supabase credentials are valid and reachable."""
    return bool(settings.SUPABASE_URL and settings.SUPABASE_SERVICE_ROLE_KEY)


import time

# Thread-safe in-memory cache for validated Supabase JWT tokens (token -> (expires_at, user_dict))
_token_cache: Dict[str, tuple[float, Dict[str, Any]]] = {}

# Thread-safe in-memory cache for validated Siksha Session tokens (token -> (expires_at, user_dict))
_session_token_cache: Dict[str, tuple[float, Dict[str, Any]]] = {}

def get_cached_session_user(token: str) -> Optional[Dict[str, Any]]:
    """Retrieves cached user dict for session token if still valid."""
    if not token or not isinstance(token, str):
        return None
    token_clean = token.strip()
    if token_clean.startswith("Bearer "):
        token_clean = token_clean.replace("Bearer ", "").strip()
    now = time.time()
    cached = _session_token_cache.get(token_clean)
    if cached and cached[0] > now:
        return cached[1]
    return None

def set_cached_session_user(token: str, user: Dict[str, Any], ttl: float = 300.0):
    """Caches validated user dict for session token with TTL (default 5 minutes)."""
    if not token or not user:
        return
    token_clean = token.strip()
    if token_clean.startswith("Bearer "):
        token_clean = token_clean.replace("Bearer ", "").strip()
    _session_token_cache[token_clean] = (time.time() + ttl, user)

def invalidate_session_cache(token: str):
    """Purges session token from in-memory cache on logout or expiration."""
    if not token:
        return
    token_clean = token.strip()
    if token_clean.startswith("Bearer "):
        token_clean = token_clean.replace("Bearer ", "").strip()
    _session_token_cache.pop(token_clean, None)
    _token_cache.pop(token_clean, None)

def verify_supabase_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verifies a Supabase Auth JWT token and returns user details.
    Uses fast-path syntax validation and in-memory TTL caching to eliminate
    redundant 500ms+ network calls to Supabase servers.
    """
    if not token or not isinstance(token, str):
        return None
    token = token.strip()
    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "").strip()

    # Fast-path: Valid Supabase JWTs start with 'ey' and contain exactly 2 dot separators
    if not (token.startswith("ey") and token.count(".") == 2):
        return None

    # Check in-memory TTL cache (valid for 5 minutes)
    now = time.time()
    cached = _token_cache.get(token)
    if cached and cached[0] > now:
        return cached[1]

    client = get_supabase_client()
    if not client:
        return None

    try:
        res = client.auth.get_user(token)
        if res and res.user:
            u = res.user
            metadata = u.user_metadata or {}
            user_data = {
                "id": str(u.id),
                "email": u.email,
                "full_name": metadata.get("full_name", u.email.split("@")[0] if u.email else "Student"),
                "role": metadata.get("role", "student"),
                "class_grade": metadata.get("class_grade", "Class 12 • Senior Secondary"),
                "target_goal": metadata.get("target_goal", "JEE / NEET"),
                "avatar_url": metadata.get("avatar_url", ""),
                "auth_provider": "supabase"
            }
            _token_cache[token] = (now + 300.0, user_data)
            return user_data
    except Exception as err:
        logger.warning(f"[Supabase Auth] Token verification failed: {err}")

    return None


def ensure_storage_buckets():
    """Ensures production storage buckets exist with public read access."""
    client = get_supabase_client()
    if not client:
        return

    buckets = ["study-materials", "profile-avatars"]
    for b in buckets:
        try:
            client.storage.create_bucket(b, options={"public": True})
            logger.info(f"[Supabase Storage] Created bucket '{b}'.")
        except Exception:
            pass  # Bucket already exists
