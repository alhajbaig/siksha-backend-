"""
SIKSHASAATHI — Supabase PostgreSQL Production Migration Engine
Migrates schema, tables, indexes, RLS policies, and all 250 questions from SQLite to Supabase PostgreSQL.
"""

import os
import sys
import json
import sqlite3
import psycopg2
from psycopg2.extras import execute_values
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent
SQLITE_DB_PATH = BASE_DIR / "data" / "siksha_saathi.db"

from dotenv import load_dotenv
load_dotenv(ROOT_DIR / ".env")

# Supabase Credentials
RAW_PW = os.getenv("SUPABASE_DB_PASSWORD", "")
HOST = os.getenv("SUPABASE_DB_HOST", "db.hmxbwitnmrjbtrozkvul.supabase.co")
PORT = int(os.getenv("SUPABASE_DB_PORT", "5432"))
DBNAME = os.getenv("SUPABASE_DB_NAME", "postgres")
USER = os.getenv("SUPABASE_DB_USER", "postgres")
DB_URL = os.getenv("SUPABASE_DB_URL", "")

def get_supabase_connection():
    if DB_URL:
        return psycopg2.connect(DB_URL, sslmode="require")
    return psycopg2.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=RAW_PW,
        dbname=DBNAME,
        sslmode="require"
    )

def get_sqlite_connection():
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

SCHEMA_DDL = """
-- 1. Enable Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- 2. Users Table
CREATE TABLE IF NOT EXISTS public.users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'student',
    class_grade TEXT DEFAULT 'Class 12 • Senior Secondary',
    target_goal TEXT DEFAULT 'JEE / NEET',
    institution TEXT DEFAULT '',
    subject TEXT DEFAULT '',
    bio TEXT DEFAULT 'Passionate STEM student exploring classical mechanics, differential calculus, and organic synthesis.',
    avatar_url TEXT DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Profiles Table (Linked to auth.users if available, or local ID)
CREATE TABLE IF NOT EXISTS public.profiles (
    id TEXT PRIMARY KEY,
    user_id TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    avatar_url TEXT DEFAULT '',
    class_level TEXT DEFAULT 'Class 12 • Senior Secondary',
    preferred_subject TEXT DEFAULT 'Physics',
    target_goal TEXT DEFAULT 'JEE / NEET',
    institution TEXT DEFAULT '',
    bio TEXT DEFAULT 'Passionate STEM student exploring classical mechanics, differential calculus, and organic synthesis.',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. User Sessions Table
CREATE TABLE IF NOT EXISTS public.user_sessions (
    token TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 5. User Telemetry Table
CREATE TABLE IF NOT EXISTS public.user_telemetry (
    user_id TEXT PRIMARY KEY,
    overall_mastery_percent REAL DEFAULT 0.0,
    active_learning_streak_days INTEGER DEFAULT 0,
    questions_solved INTEGER DEFAULT 0,
    socratic_dialogues_count INTEGER DEFAULT 0,
    subject_mastery_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    knowledge_frontier_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 6. Practice Subjects Table (5 core subjects: bio, phys, math, chem, cs)
CREATE TABLE IF NOT EXISTS public.practice_subjects (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    icon TEXT NOT NULL,
    order_index INTEGER DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 7. Practice Levels Table (5 levels per subject = 25 levels)
CREATE TABLE IF NOT EXISTS public.practice_levels (
    id TEXT PRIMARY KEY,
    subject_id TEXT NOT NULL REFERENCES public.practice_subjects (id) ON DELETE CASCADE,
    level_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    question_count INTEGER DEFAULT 10,
    order_index INTEGER DEFAULT 1
);

-- 8. Practice Questions Table (250 curated MCQs)
CREATE TABLE IF NOT EXISTS public.practice_questions (
    id TEXT PRIMARY KEY,
    subject_id TEXT NOT NULL REFERENCES public.practice_subjects (id) ON DELETE CASCADE,
    level_number INTEGER NOT NULL,
    order_index INTEGER NOT NULL,
    topic TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    question_text TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_option INTEGER NOT NULL,
    explanation TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 9. Quiz Attempts Table
CREATE TABLE IF NOT EXISTS public.quiz_attempts (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    subject_id TEXT NOT NULL REFERENCES public.practice_subjects (id) ON DELETE CASCADE,
    level_number INTEGER NOT NULL,
    score INTEGER NOT NULL,
    total_questions INTEGER NOT NULL,
    accuracy_percent REAL NOT NULL,
    time_spent_seconds INTEGER DEFAULT 0,
    completed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 10. Quiz Answers Table
CREATE TABLE IF NOT EXISTS public.quiz_answers (
    id BIGSERIAL PRIMARY KEY,
    attempt_id TEXT NOT NULL REFERENCES public.quiz_attempts (id) ON DELETE CASCADE,
    user_id TEXT NOT NULL,
    question_id TEXT NOT NULL REFERENCES public.practice_questions (id) ON DELETE CASCADE,
    selected_option INTEGER NOT NULL,
    correct_option INTEGER NOT NULL,
    is_correct INTEGER NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 11. Notes Table
CREATE TABLE IF NOT EXISTS public.notes (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    subject TEXT NOT NULL,
    subject_badge TEXT NOT NULL,
    format TEXT NOT NULL,
    file_path TEXT,
    file_type TEXT,
    file_size INTEGER DEFAULT 0,
    body TEXT NOT NULL,
    word_count INTEGER DEFAULT 0,
    reading_time_min INTEGER DEFAULT 1,
    chunk_count INTEGER DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'indexed',
    error_message TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 12. Note Chunks with Vector Embeddings (pgvector)
CREATE TABLE IF NOT EXISTS public.note_chunks (
    id BIGSERIAL PRIMARY KEY,
    note_id TEXT NOT NULL REFERENCES public.notes (id) ON DELETE CASCADE,
    user_id TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    text TEXT NOT NULL,
    page_number INTEGER DEFAULT 1,
    section_title TEXT DEFAULT '',
    token_count INTEGER DEFAULT 0,
    embedding vector(1536),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 13. RAG Query History Table
CREATE TABLE IF NOT EXISTS public.rag_queries (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    note_id TEXT NOT NULL,
    query TEXT NOT NULL,
    query_type TEXT DEFAULT 'custom',
    answer TEXT NOT NULL,
    citations_json JSONB,
    retrieval_time_ms REAL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 14. AI Learning Roadmaps Table
CREATE TABLE IF NOT EXISTS public.ai_learning_roadmaps (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    goal TEXT NOT NULL,
    estimated_duration TEXT NOT NULL,
    progress_snapshot_hash TEXT NOT NULL,
    roadmap_json JSONB NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 15. AI Conversations Table
CREATE TABLE IF NOT EXISTS public.ai_conversations (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    chapter_id TEXT,
    title TEXT NOT NULL,
    mode TEXT DEFAULT 'socratic',
    subject TEXT DEFAULT '',
    persona TEXT DEFAULT 'balanced',
    summary TEXT DEFAULT '',
    conversation_type TEXT DEFAULT 'notes',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 16. AI Messages Table
CREATE TABLE IF NOT EXISTS public.ai_messages (
    id TEXT PRIMARY KEY,
    conversation_id TEXT NOT NULL REFERENCES public.ai_conversations (id) ON DELETE CASCADE,
    sender TEXT NOT NULL,
    text TEXT NOT NULL,
    metadata_json JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for lightning performance
CREATE INDEX IF NOT EXISTS idx_practice_questions_subj_lvl ON public.practice_questions (subject_id, level_number);
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_user ON public.quiz_attempts (user_id, subject_id);
CREATE INDEX IF NOT EXISTS idx_quiz_answers_user_q ON public.quiz_answers (user_id, question_id);
CREATE INDEX IF NOT EXISTS idx_notes_user_subject ON public.notes (user_id, subject);

-- Row Level Security (RLS)
ALTER TABLE public.practice_subjects ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.practice_levels ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.practice_questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.quiz_attempts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.quiz_answers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_telemetry ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.notes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ai_learning_roadmaps ENABLE ROW LEVEL SECURITY;

-- Publicly readable curriculum & questions
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = 'practice_subjects' AND policyname = 'Allow public read practice_subjects') THEN
        CREATE POLICY "Allow public read practice_subjects" ON public.practice_subjects FOR SELECT USING (true);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = 'practice_levels' AND policyname = 'Allow public read practice_levels') THEN
        CREATE POLICY "Allow public read practice_levels" ON public.practice_levels FOR SELECT USING (true);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = 'practice_questions' AND policyname = 'Allow public read practice_questions') THEN
        CREATE POLICY "Allow public read practice_questions" ON public.practice_questions FOR SELECT USING (true);
    END IF;
END $$;
"""

def migrate():
    print("=== Starting Supabase PostgreSQL Migration ===")
    pg_conn = get_supabase_connection()
    pg_cur = pg_conn.cursor()
    
    sqlite_conn = get_sqlite_connection()
    sqlite_cur = sqlite_conn.cursor()

    # 1. Execute DDL
    print("Creating tables, extensions, indexes, and RLS policies on Supabase...")
    pg_cur.execute(SCHEMA_DDL)
    pg_conn.commit()
    print("Schema DDL applied successfully!")

    # 2. Migrate Practice Subjects
    print("\nMigrating practice_subjects...")
    sqlite_cur.execute("SELECT id, title, description, icon, order_index FROM practice_subjects ORDER BY order_index ASC")
    subjects = [dict(r) for r in sqlite_cur.fetchall()]
    print(f"Found {len(subjects)} subjects in SQLite.")
    for s in subjects:
        pg_cur.execute("""
        INSERT INTO public.practice_subjects (id, title, description, icon, order_index)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            title = EXCLUDED.title,
            description = EXCLUDED.description,
            icon = EXCLUDED.icon,
            order_index = EXCLUDED.order_index;
        """, (s["id"], s["title"], s["description"], s["icon"], s["order_index"]))
    pg_conn.commit()
    print("Practice subjects migrated.")

    # 3. Migrate Practice Levels
    print("\nMigrating practice_levels...")
    sqlite_cur.execute("SELECT id, subject_id, level_number, title, description, question_count, order_index FROM practice_levels ORDER BY order_index ASC")
    levels = [dict(r) for r in sqlite_cur.fetchall()]
    print(f"Found {len(levels)} levels in SQLite.")
    for l in levels:
        pg_cur.execute("""
        INSERT INTO public.practice_levels (id, subject_id, level_number, title, description, question_count, order_index)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            title = EXCLUDED.title,
            description = EXCLUDED.description,
            question_count = EXCLUDED.question_count;
        """, (l["id"], l["subject_id"], l["level_number"], l["title"], l["description"], l["question_count"], l["order_index"]))
    pg_conn.commit()
    print("Practice levels migrated.")

    # 4. Migrate Practice Questions (All 250 Questions)
    print("\nMigrating practice_questions (250 questions across 5 subjects)...")
    sqlite_cur.execute("""
    SELECT id, subject_id, level_number, order_index, topic, difficulty, question_text, option_a, option_b, option_c, option_d, correct_option, explanation 
    FROM practice_questions ORDER BY subject_id, level_number, order_index
    """)
    questions = [dict(r) for r in sqlite_cur.fetchall()]
    print(f"Found {len(questions)} questions in SQLite.")
    
    def clean(val):
        if isinstance(val, str):
            return val.replace('\x00', '')
        return val

    q_data = [
        (
            clean(q["id"]), clean(q["subject_id"]), q["level_number"], q["order_index"],
            clean(q["topic"]), clean(q["difficulty"]), clean(q["question_text"]),
            clean(q["option_a"]), clean(q["option_b"]), clean(q["option_c"]), clean(q["option_d"]),
            q["correct_option"], clean(q["explanation"])
        )
        for q in questions
    ]
    
    insert_query = """
    INSERT INTO public.practice_questions (
        id, subject_id, level_number, order_index, topic, difficulty,
        question_text, option_a, option_b, option_c, option_d,
        correct_option, explanation
    ) VALUES %s
    ON CONFLICT (id) DO UPDATE SET
        question_text = EXCLUDED.question_text,
        option_a = EXCLUDED.option_a,
        option_b = EXCLUDED.option_b,
        option_c = EXCLUDED.option_c,
        option_d = EXCLUDED.option_d,
        correct_option = EXCLUDED.correct_option,
        explanation = EXCLUDED.explanation;
    """
    execute_values(pg_cur, insert_query, q_data)
    pg_conn.commit()
    print(f"Successfully migrated {len(questions)} questions to Supabase PostgreSQL!")

    # 5. Migrate Users & Profiles
    print("\nMigrating seeded users & profiles...")
    sqlite_cur.execute("SELECT * FROM users")
    users = [dict(r) for r in sqlite_cur.fetchall()]
    for u in users:
        pg_cur.execute("""
        INSERT INTO public.users (id, email, password_hash, salt, full_name, role, class_grade, target_goal, institution, subject, bio, avatar_url, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        ON CONFLICT (id) DO NOTHING;
        """, (u["id"], u["email"], u["password_hash"], u["salt"], u["full_name"], u["role"], u["class_grade"], u["target_goal"], u.get("institution", ""), u.get("subject", ""), u.get("bio", ""), u.get("avatar_url", "")))
    
    sqlite_cur.execute("SELECT * FROM profiles")
    profiles = [dict(r) for r in sqlite_cur.fetchall()]
    for p in profiles:
        pg_cur.execute("""
        INSERT INTO public.profiles (id, user_id, full_name, email, avatar_url, class_level, preferred_subject, target_goal, institution, bio, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        ON CONFLICT (id) DO NOTHING;
        """, (p["id"], p["user_id"], p["full_name"], p["email"], p.get("avatar_url", ""), p.get("class_level", ""), p.get("preferred_subject", ""), p.get("target_goal", ""), p.get("institution", ""), p.get("bio", "")))

    pg_conn.commit()
    print("Users & profiles migrated.")

    # 6. Verify in Supabase
    pg_cur.execute("SELECT count(*) FROM public.practice_subjects;")
    subj_count = pg_cur.fetchone()[0]
    pg_cur.execute("SELECT count(*) FROM public.practice_levels;")
    lvl_count = pg_cur.fetchone()[0]
    pg_cur.execute("SELECT count(*) FROM public.practice_questions;")
    q_count = pg_cur.fetchone()[0]
    pg_cur.execute("SELECT count(*) FROM public.practice_questions WHERE subject_id='bio';")
    bio_q_count = pg_cur.fetchone()[0]

    print("\n=== SUPABASE POSTGRESQL VERIFICATION ===")
    print(f"  practice_subjects count : {subj_count} (Expected: 5)")
    print(f"  practice_levels count   : {lvl_count} (Expected: 25)")
    print(f"  practice_questions count: {q_count} (Expected: 250)")
    print(f"  biology questions count : {bio_q_count} (Expected: 50)")

    pg_cur.close()
    pg_conn.close()
    sqlite_cur.close()
    sqlite_conn.close()
    print("\n Migration completed successfully!")

if __name__ == "__main__":
    migrate()
