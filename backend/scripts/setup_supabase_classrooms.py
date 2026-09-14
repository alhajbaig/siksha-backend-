"""
SIKSHASAATHI — Supabase PostgreSQL Production Classroom Schema Setup
Creates public.classrooms and public.classroom_members with unique constraints,
indexes, and Row Level Security (RLS) policies.
Authoritative cloud schema adhering to Siksha Saathi user identity standards.
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("SUPABASE_DB_URL")
if not DB_URL:
    raise RuntimeError("SUPABASE_DB_URL is not set in environment!")

DDL_SQL = """
-- 1. Classrooms Table
CREATE TABLE IF NOT EXISTS public.classrooms (
    id TEXT PRIMARY KEY,
    teacher_id TEXT NOT NULL,
    name TEXT NOT NULL,
    subject TEXT NOT NULL,
    grade_level TEXT NOT NULL DEFAULT 'Class 12',
    description TEXT DEFAULT '',
    join_code TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    is_active SMALLINT NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Ensure case-insensitive unique index on join_code
CREATE UNIQUE INDEX IF NOT EXISTS idx_classrooms_join_code_upper 
ON public.classrooms (UPPER(join_code));

-- Index for teacher's classrooms
CREATE INDEX IF NOT EXISTS idx_classrooms_teacher_status 
ON public.classrooms (teacher_id, status, is_active);

-- 2. Classroom Memberships Table
CREATE TABLE IF NOT EXISTS public.classroom_members (
    id BIGSERIAL PRIMARY KEY,
    classroom_id TEXT NOT NULL REFERENCES public.classrooms(id) ON DELETE CASCADE,
    student_id TEXT NOT NULL,
    joined_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status TEXT NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_classroom_student UNIQUE (classroom_id, student_id)
);

-- Indexes for lightning lookups
CREATE INDEX IF NOT EXISTS idx_members_student_status 
ON public.classroom_members (student_id, status);

CREATE INDEX IF NOT EXISTS idx_members_classroom_status 
ON public.classroom_members (classroom_id, status);

-- 3. Row Level Security (RLS)
ALTER TABLE public.classrooms ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.classroom_members ENABLE ROW LEVEL SECURITY;

-- Classrooms Policies
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = 'classrooms' AND policyname = 'Service role full access on classrooms') THEN
        CREATE POLICY "Service role full access on classrooms" 
        ON public.classrooms FOR ALL 
        USING (true) WITH CHECK (true);
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = 'classrooms' AND policyname = 'Allow read active classrooms') THEN
        CREATE POLICY "Allow read active classrooms" 
        ON public.classrooms FOR SELECT 
        USING (is_active = 1 AND status = 'active');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = 'classrooms' AND policyname = 'Teacher manage own classrooms') THEN
        CREATE POLICY "Teacher manage own classrooms"
        ON public.classrooms FOR ALL
        TO authenticated
        USING (teacher_id = (auth.uid())::text)
        WITH CHECK (teacher_id = (auth.uid())::text);
    END IF;

    -- Classroom Members Policies
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = 'classroom_members' AND policyname = 'Service role full access on members') THEN
        CREATE POLICY "Service role full access on members" 
        ON public.classroom_members FOR ALL 
        USING (true) WITH CHECK (true);
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = 'classroom_members' AND policyname = 'Students read own memberships') THEN
        CREATE POLICY "Students read own memberships" 
        ON public.classroom_members FOR SELECT 
        TO authenticated
        USING (student_id = (auth.uid())::text);
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = 'classroom_members' AND policyname = 'Teachers read enrolled students') THEN
        CREATE POLICY "Teachers read enrolled students"
        ON public.classroom_members FOR SELECT 
        TO authenticated
        USING (
            classroom_id IN (
                SELECT id FROM public.classrooms WHERE teacher_id = (auth.uid())::text
            )
        );
    END IF;
END $$;
"""

def setup_classrooms():
    print("Connecting to Supabase PostgreSQL...")
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = False
    cur = conn.cursor()

    try:
        print("Executing DDL for public.classrooms and public.classroom_members...")
        cur.execute(DDL_SQL)
        conn.commit()
        print("Classrooms and classroom_members tables and indexes created successfully in Supabase!")

        # Verify tables
        cur.execute("""
            SELECT table_name, column_name, data_type 
            FROM information_schema.columns 
            WHERE table_schema = 'public' AND table_name IN ('classrooms', 'classroom_members')
            ORDER BY table_name, ordinal_position;
        """)
        rows = cur.fetchall()
        print(f"\nVerified {len(rows)} columns across classrooms and classroom_members:")
        for r in rows:
            print(f"  {r[0]}.{r[1]} ({r[2]})")

    except Exception as e:
        conn.rollback()
        print("Error during setup:", e)
        raise
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    setup_classrooms()
