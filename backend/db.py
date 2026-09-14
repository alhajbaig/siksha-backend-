"""
SIKHSAATHI — Persistent Database Module for Notes & Vector Knowledge Base
Handles SQLite schema, connection management, user-isolated CRUD, and initial note seeding.
"""

import os
import json
import sqlite3
import hashlib
import secrets
import uuid
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

logger = logging.getLogger("siksha_saathi.db")

# Serverless & Vercel environment detection
is_serverless = bool(
    os.environ.get("VERCEL") or 
    os.environ.get("AWS_LAMBDA_FUNCTION_NAME") or 
    os.environ.get("LAMBDA_TASK_ROOT")
)

if is_serverless:
    DB_DIR = "/tmp/data"
    STORAGE_DIR = "/tmp/storage/uploads"
else:
    DB_DIR = os.path.join(os.path.dirname(__file__), "data")
    STORAGE_DIR = os.path.join(os.path.dirname(__file__), "storage", "uploads")

try:
    os.makedirs(DB_DIR, exist_ok=True)
    os.makedirs(STORAGE_DIR, exist_ok=True)
except (OSError, PermissionError):
    DB_DIR = "/tmp/data"
    STORAGE_DIR = "/tmp/storage/uploads"
    os.makedirs(DB_DIR, exist_ok=True)
    os.makedirs(STORAGE_DIR, exist_ok=True)

DB_PATH = os.path.join(DB_DIR, "siksha_saathi.db")

# In serverless environments, copy the seed database from repository if available
if is_serverless and not os.path.exists(DB_PATH):
    seed_db = os.path.join(os.path.dirname(__file__), "data", "siksha_saathi.db")
    if os.path.exists(seed_db):
        try:
            import shutil
            shutil.copy2(seed_db, DB_PATH)
        except Exception as _e:
            pass


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 60000")
    try:
        conn.execute("PRAGMA journal_mode = WAL")
    except Exception:
        pass
    return conn


def hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
    """Hashes a password with PBKDF2-HMAC-SHA256 and unique salt."""
    if not salt:
        salt = secrets.token_hex(16)
    pw_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000).hex()
    return pw_hash, salt


def verify_password(password: str, password_hash: str, salt: str) -> bool:
    """Verifies a plain text password against stored hash and salt."""
    expected_hash, _ = hash_password(password, salt)
    return secrets.compare_digest(expected_hash, password_hash)


def init_db():
    """Initializes SQLite database tables for users, sessions, telemetry, notes, chunks, and RAG queries."""
    conn = get_db_connection()
    try:
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = NORMAL")
    except Exception:
        pass
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
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
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    """)

    # User Profiles table (Strict relational profile linked to authenticated user)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
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
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    # User Sessions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_sessions (
        token TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        expires_at TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    # User Telemetry / Mastery table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_telemetry (
        user_id TEXT PRIMARY KEY,
        overall_mastery_percent REAL DEFAULT 0.0,
        active_learning_streak_days INTEGER DEFAULT 0,
        questions_solved INTEGER DEFAULT 0,
        socratic_dialogues_count INTEGER DEFAULT 0,
        subject_mastery_json TEXT NOT NULL,
        knowledge_frontier_json TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    # Notes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
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
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    """)

    # Note chunks table with embedding JSON
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS note_chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        note_id TEXT NOT NULL,
        user_id TEXT NOT NULL,
        chunk_index INTEGER NOT NULL,
        text TEXT NOT NULL,
        page_number INTEGER DEFAULT 1,
        section_title TEXT DEFAULT '',
        token_count INTEGER DEFAULT 0,
        embedding TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (note_id) REFERENCES notes (id) ON DELETE CASCADE
    );
    """)

    # RAG query history table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rag_queries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        note_id TEXT NOT NULL,
        query TEXT NOT NULL,
        query_type TEXT DEFAULT 'custom',
        answer TEXT NOT NULL,
        citations_json TEXT,
        retrieval_time_ms REAL,
        created_at TEXT NOT NULL
    );
    """)

    # Practice Subjects table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS practice_subjects (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        icon TEXT NOT NULL,
        order_index INTEGER DEFAULT 1
    );
    """)

    # Practice Levels table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS practice_levels (
        id TEXT PRIMARY KEY,
        subject_id TEXT NOT NULL,
        level_number INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        question_count INTEGER DEFAULT 10,
        order_index INTEGER DEFAULT 1,
        FOREIGN KEY (subject_id) REFERENCES practice_subjects (id) ON DELETE CASCADE
    );
    """)

    # Practice Questions table (200 Master Questions Bank)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS practice_questions (
        id TEXT PRIMARY KEY,
        subject_id TEXT NOT NULL,
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
        FOREIGN KEY (subject_id) REFERENCES practice_subjects (id) ON DELETE CASCADE
    );
    """)

    # Quiz Attempts table (Recorded per completed 10-question quiz)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_attempts (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        subject_id TEXT NOT NULL,
        level_number INTEGER NOT NULL,
        score INTEGER NOT NULL,
        total_questions INTEGER NOT NULL,
        accuracy_percent REAL NOT NULL,
        time_spent_seconds INTEGER DEFAULT 0,
        completed_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    # Individual Question Answers for detailed review & analytics
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        attempt_id TEXT NOT NULL,
        user_id TEXT NOT NULL,
        question_id TEXT NOT NULL,
        selected_option INTEGER NOT NULL,
        correct_option INTEGER NOT NULL,
        is_correct INTEGER NOT NULL,
        FOREIGN KEY (attempt_id) REFERENCES quiz_attempts (id) ON DELETE CASCADE
    );
    """)

    # Diagnostic Assessment Attempts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assessment_attempts (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        assessment_id TEXT NOT NULL,
        title TEXT NOT NULL,
        score INTEGER NOT NULL,
        max_score INTEGER NOT NULL,
        accuracy_percent REAL NOT NULL,
        percentile REAL NOT NULL,
        time_spent_seconds INTEGER DEFAULT 0,
        subject_breakdown_json TEXT NOT NULL,
        solutions_json TEXT NOT NULL,
        completed_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    # AI Personalized Roadmaps table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_learning_roadmaps (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        title TEXT NOT NULL,
        summary TEXT NOT NULL,
        goal TEXT NOT NULL,
        estimated_duration TEXT NOT NULL,
        progress_snapshot_hash TEXT NOT NULL,
        roadmap_json TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'active',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    # AI Conversations for Notes AI Q&A + AI Mentor
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_conversations (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        chapter_id TEXT,
        title TEXT NOT NULL,
        mode TEXT DEFAULT 'socratic',
        subject TEXT DEFAULT '',
        persona TEXT DEFAULT 'balanced',
        summary TEXT DEFAULT '',
        conversation_type TEXT DEFAULT 'notes',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    # AI Messages for Multi-turn Contextual Follow-up
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_messages (
        id TEXT PRIMARY KEY,
        conversation_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        mode TEXT DEFAULT '',
        source_json TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (conversation_id) REFERENCES ai_conversations (id) ON DELETE CASCADE
    );
    """)

    # User AI Preferences for Mentor Persona & Study Settings
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_ai_preferences (
        user_id TEXT PRIMARY KEY,
        persona TEXT DEFAULT 'balanced',
        daily_study_minutes INTEGER DEFAULT 45,
        preferred_language TEXT DEFAULT 'en',
        updated_at TEXT NOT NULL DEFAULT '',
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    # Smart Revision Sessions table (Persists completed smart revision journeys)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS revision_sessions (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        topic TEXT NOT NULL,
        subject_id TEXT NOT NULL,
        priority_score REAL DEFAULT 0.0,
        status TEXT NOT NULL DEFAULT 'completed',
        duration_minutes REAL NOT NULL DEFAULT 0.0,
        steps_total INTEGER NOT NULL DEFAULT 4,
        steps_completed INTEGER NOT NULL DEFAULT 4,
        score INTEGER DEFAULT 0,
        total_questions INTEGER DEFAULT 0,
        review_mode TEXT DEFAULT 'standard',
        resources_used_json TEXT DEFAULT '[]',
        created_at TEXT NOT NULL,
        completed_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    # Emergency Sessions table (Emergency Mode focused study plans)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emergency_sessions (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        exam_name TEXT DEFAULT '',
        exam_date TEXT DEFAULT '',
        available_minutes INTEGER NOT NULL,
        subject_focus TEXT DEFAULT 'all',
        plan_json TEXT NOT NULL DEFAULT '{}',
        status TEXT NOT NULL DEFAULT 'active',
        steps_completed INTEGER DEFAULT 0,
        steps_total INTEGER DEFAULT 0,
        topics_covered_json TEXT DEFAULT '[]',
        performance_json TEXT DEFAULT '{}',
        created_at TEXT NOT NULL,
        completed_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    # Classrooms table (Foundation for Teacher ↔ Student Classroom Ecosystem)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS classrooms (
        id TEXT PRIMARY KEY,
        teacher_id TEXT NOT NULL,
        name TEXT NOT NULL,
        subject TEXT NOT NULL,
        grade_level TEXT NOT NULL,
        description TEXT DEFAULT '',
        join_code TEXT UNIQUE NOT NULL,
        is_active INTEGER DEFAULT 1,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (teacher_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    # Classroom Memberships table (Referential relationship linking students to classrooms)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS classroom_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        classroom_id TEXT NOT NULL,
        student_id TEXT NOT NULL,
        joined_at TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'active',
        UNIQUE(classroom_id, student_id),
        FOREIGN KEY (classroom_id) REFERENCES classrooms (id) ON DELETE CASCADE,
        FOREIGN KEY (student_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    # Classroom Announcements table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS classroom_announcements (
        id TEXT PRIMARY KEY,
        classroom_id TEXT NOT NULL,
        author_name TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        tag TEXT NOT NULL DEFAULT 'General',
        is_pinned INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY (classroom_id) REFERENCES classrooms (id) ON DELETE CASCADE
    );
    """)

    # Classroom Materials & Uploaded Notes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS classroom_materials (
        id TEXT PRIMARY KEY,
        classroom_id TEXT NOT NULL,
        subject TEXT NOT NULL,
        title TEXT NOT NULL,
        topic TEXT NOT NULL DEFAULT 'General',
        file_type TEXT NOT NULL DEFAULT 'PDF',
        read_time TEXT NOT NULL DEFAULT '10 mins',
        summary TEXT NOT NULL,
        content TEXT,
        download_url TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (classroom_id) REFERENCES classrooms (id) ON DELETE CASCADE
    );
    """)

    # Classroom Doubts & Q&A Desk table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS classroom_doubts (
        id TEXT PRIMARY KEY,
        classroom_id TEXT NOT NULL,
        student_id TEXT NOT NULL,
        student_name TEXT NOT NULL,
        question TEXT NOT NULL,
        topic TEXT NOT NULL DEFAULT 'General',
        ai_hint TEXT,
        teacher_reply TEXT,
        status TEXT NOT NULL DEFAULT 'open',
        created_at TEXT NOT NULL,
        FOREIGN KEY (classroom_id) REFERENCES classrooms (id) ON DELETE CASCADE
    );
    """)

    # Schema migration: add columns if missing (safe for existing DBs)
    # Must run BEFORE index creation to ensure new columns exist
    _safe_add_columns(conn)

    # Create indexes for fast lookup and user isolation
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_profiles_user ON profiles(user_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(token);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user ON user_sessions(user_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_notes_user ON notes(user_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_notes_subject ON notes(user_id, subject);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_note ON note_chunks(note_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_user ON note_chunks(user_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_pq_subj_lvl ON practice_questions(subject_id, level_number);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_attempts_user ON quiz_attempts(user_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_attempts_user_subj ON quiz_attempts(user_id, subject_id, level_number);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_answers_attempt ON quiz_answers(attempt_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_answers_user ON quiz_answers(user_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_answers_question ON quiz_answers(question_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_roadmaps_user ON ai_learning_roadmaps(user_id, status);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ai_conv_user ON ai_conversations(user_id, chapter_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ai_conv_type ON ai_conversations(user_id, conversation_type);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ai_messages_conv ON ai_messages(conversation_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ai_prefs_user ON user_ai_preferences(user_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_rev_user ON revision_sessions(user_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_rev_user_topic ON revision_sessions(user_id, topic);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_rev_user_date ON revision_sessions(user_id, completed_at);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_asmt_user ON assessment_attempts(user_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_asmt_assessment ON assessment_attempts(assessment_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_emg_user ON emergency_sessions(user_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_emg_status ON emergency_sessions(user_id, status);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cls_teacher ON classrooms(teacher_id, is_active);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cls_code ON classrooms(join_code);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cm_class ON classroom_members(classroom_id, status);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cm_student ON classroom_members(student_id, status);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ca_class ON classroom_announcements(classroom_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cm_class_mat ON classroom_materials(classroom_id, subject);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cd_class_dbt ON classroom_doubts(classroom_id, created_at);")

    conn.commit()
    conn.close()


def seed_default_notes_for_user(user_id: str):
    """Seeds the 4 default curriculum notes for a user if they don't have any notes yet."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM notes WHERE user_id = ?", (user_id,))
    count = cursor.fetchone()[0]

    if count > 0:
        conn.close()
        return

    now = datetime.utcnow().isoformat()

    default_notes = [
        {
            "id": f"{user_id}_note_1",
            "user_id": user_id,
            "title": "Organic Chemistry: Reaction Mechanisms (SN1 vs SN2)",
            "subject": "chem",
            "subject_badge": "CHEMISTRY",
            "format": "PDF • 14 CHUNKS",
            "file_type": "pdf",
            "body": """<h3>1. Overview of Nucleophilic Substitution</h3>
<p>Nucleophilic substitution involves replacing a leaving group with an electron-rich nucleophile on an <em>sp</em><sup>3</sup> hybridized carbon center.</p>

<div class="formula-block">
  <strong>Rate Laws & Kinetics:</strong><br>
  SN1 Rate = <em>k</em>[Substrate] &nbsp;(First order, unimolecular, racemization occurs)<br>
  SN2 Rate = <em>k</em>[Substrate][Nucleophile] &nbsp;(Second order, bimolecular, Walden inversion)
</div>

<h3>2. Key Differences Matrix</h3>
<ul style="padding-left: 1.25rem; display: flex; flex-direction: column; gap: 6px;">
  <li><strong style="color: var(--text-main);">Substrate preference:</strong> 3° &gt; 2° &gt; 1° for SN1 due to carbocation stabilization. 1° &gt; 2° &gt; 3° for SN2 due to steric hindrance to backside attack.</li>
  <li><strong style="color: var(--text-main);">Solvent Effects:</strong> Polar protic solvents (e.g., H<sub>2</sub>O, EtOH) stabilize ionic carbocations and favor SN1. Polar aprotic solvents (e.g., Acetone, DMSO) leave nucleophiles unhindered and favor SN2.</li>
  <li><strong style="color: var(--text-main);">Stereochemistry:</strong> SN1 produces partial racemization due to planar carbocation intermediate. SN2 results in <span class="rag-highlight-segment">100% stereochemical Walden inversion</span>.</li>
</ul>

<h3>3. High-Yield Exam Pitfalls</h3>
<p>Allylic and benzylic substrates can undergo rapid SN1 reactions even if nominally primary, due to strong resonance delocalization of the carbocation.</p>""",
            "word_count": 310,
            "reading_time_min": 4,
            "chunk_count": 4,
            "status": "indexed",
            "chunks": [
                {
                    "text": "Nucleophilic substitution involves replacing a leaving group with an electron-rich nucleophile on an sp3 hybridized carbon center. SN1 reactions occur in 2 steps via a planar carbocation intermediate.",
                    "page_number": 1,
                    "section_title": "Overview & Mechanism"
                },
                {
                    "text": "Rate Laws: SN1 Rate = k[Substrate] (First order, unimolecular, racemization). SN2 Rate = k[Substrate][Nucleophile] (Second order, bimolecular, Walden inversion).",
                    "page_number": 1,
                    "section_title": "Kinetics & Rate Laws"
                },
                {
                    "text": "Substrate Preference: 3° > 2° > 1° for SN1 (carbocation stability). 1° > 2° > 3° for SN2 (steric hindrance to backside attack).",
                    "page_number": 2,
                    "section_title": "Substrate Effects"
                },
                {
                    "text": "Solvent Effects: Polar protic solvents (H2O, EtOH) stabilize carbocations and favor SN1. Polar aprotic solvents (Acetone, DMSO) leave nucleophiles unhindered and favor SN2. Allylic and benzylic substrates accelerate SN1 due to resonance.",
                    "page_number": 2,
                    "section_title": "Solvents & Exam Pitfalls"
                }
            ]
        },
        {
            "id": f"{user_id}_note_2",
            "user_id": user_id,
            "title": "Newtonian Mechanics & Free Body Diagrams",
            "subject": "phys",
            "subject_badge": "PHYSICS",
            "format": "SCAN • 10 CHUNKS",
            "file_type": "png",
            "body": """<h3>1. Newton's 3 Fundamental Laws</h3>
<p>Foundation of classical mechanics governing macroscopic motion at non-relativistic velocities.</p>

<div class="formula-block">
  Second Law: ∑ <strong>F</strong> = <em>m</em><strong>a</strong> = <em>d</em><strong>p</strong>/<em>dt</em><br>
  Third Law: <strong>F</strong><sub>AB</sub> = −<strong>F</strong><sub>BA</sub>
</div>

<h3>2. Free Body Diagram (FBD) Rules</h3>
<ul style="padding-left: 1.25rem; display: flex; flex-direction: column; gap: 6px;">
  <li>Isolate the object as a point mass.</li>
  <li>Draw only external forces acting directly ON the object.</li>
  <li>Establish an orthogonal coordinate axis aligned with expected acceleration.</li>
</ul>

<h3>3. Damped Harmonic Oscillations</h3>
<p>Underdamped motion decay amplitude: <em>A(t) = A<sub>0</sub> e<sup>−γt</sup></em> where <em>γ = b/(2m)</em> and angular frequency <em>ω = √(ω<sub>0</sub><sup>2</sup> − γ<sup>2</sup>)</em>.</p>""",
            "word_count": 280,
            "reading_time_min": 3,
            "chunk_count": 3,
            "status": "indexed",
            "chunks": [
                {
                    "text": "Newton's Second Law states that the net external force on a body is equal to the time rate of change of linear momentum: F_net = m*a = dp/dt.",
                    "page_number": 1,
                    "section_title": "Laws of Motion"
                },
                {
                    "text": "Free Body Diagram Rules: Isolate the object as a point mass, draw only external forces acting directly on it, and establish coordinate axes aligned with expected acceleration.",
                    "page_number": 1,
                    "section_title": "FBD Strategy"
                },
                {
                    "text": "Damped Harmonic Oscillator: Differential equation is m*(d²x/dt²) + b*(dx/dt) + k*x = 0. Underdamped amplitude decays as A(t) = A_0 * exp(-gamma * t) with gamma = b/(2m).",
                    "page_number": 2,
                    "section_title": "Damped Oscillations"
                }
            ]
        },
        {
            "id": f"{user_id}_note_3",
            "user_id": user_id,
            "title": "Calculus: Integration by Parts & Partial Fractions",
            "subject": "math",
            "subject_badge": "MATHEMATICS",
            "format": "MD • 12 CHUNKS",
            "file_type": "md",
            "body": """<h3>1. Integration by Parts Formula</h3>
<div class="formula-block">
  ∫ <em>u dv</em> = <em>uv</em> − ∫ <em>v du</em>
</div>
<p>Use the <strong>ILATE</strong> priority rule to select <em>u</em>:</p>
<ol style="padding-left: 1.25rem; margin: 0.5rem 0; display: flex; flex-direction: column; gap: 4px;">
  <li><strong>I:</strong> Inverse Trigonometric</li>
  <li><strong>L:</strong> Logarithmic</li>
  <li><strong>A:</strong> Algebraic</li>
  <li><strong>T:</strong> Trigonometric</li>
  <li><strong>E:</strong> Exponential</li>
</ol>

<h3>2. Partial Fraction Decomposition</h3>
<p>Decompose rational functions P(x)/Q(x) into linear terms A/(x-a) and irreducible quadratic terms (Bx+C)/(x² + bx + c).</p>""",
            "word_count": 250,
            "reading_time_min": 3,
            "chunk_count": 3,
            "status": "indexed",
            "chunks": [
                {
                    "text": "Integration by Parts Formula: Integral of u dv = u*v - Integral of v du. Derived from product rule of differentiation.",
                    "page_number": 1,
                    "section_title": "Integration by Parts"
                },
                {
                    "text": "ILATE Priority Rule for choosing u: Inverse Trigonometric > Logarithmic > Algebraic > Trigonometric > Exponential.",
                    "page_number": 1,
                    "section_title": "ILATE Rule"
                },
                {
                    "text": "Partial Fraction Decomposition: Distinct linear factors (x-a) produce terms A/(x-a). Irreducible quadratic factors (x^2+bx+c) produce (Bx+C)/(x^2+bx+c).",
                    "page_number": 2,
                    "section_title": "Partial Fractions"
                }
            ]
        },
        {
            "id": f"{user_id}_note_4",
            "user_id": user_id,
            "title": "Data Structures: Red-Black Trees & Invariants",
            "subject": "cs",
            "subject_badge": "COMP SCIENCE",
            "format": "MD • 12 CHUNKS",
            "file_type": "md",
            "body": """<h3>1. Red-Black Tree Invariants</h3>
<p>A self-balancing Binary Search Tree where each node contains an extra color bit (Red or Black).</p>
<ul style="padding-left: 1.25rem; display: flex; flex-direction: column; gap: 6px;">
  <li><strong>Property 1:</strong> Every node is either red or black.</li>
  <li><strong>Property 2:</strong> The root is always black.</li>
  <li><strong>Property 3:</strong> Red nodes cannot have red children (no consecutive reds).</li>
  <li><strong>Property 4:</strong> Every path from root to NIL leaves contains equal black-height.</li>
</ul>

<h3>2. Complexity Guarantees</h3>
<p>Maximum height of Red-Black Tree is <em>2 × log₂(N + 1)</em>, guaranteeing <strong>O(log N)</strong> worst-case search, insertion, and deletion.</p>""",
            "word_count": 270,
            "reading_time_min": 3,
            "chunk_count": 2,
            "status": "indexed",
            "chunks": [
                {
                    "text": "Red-Black Tree is a self-balancing BST with properties: Root is black, no consecutive red nodes, and equal black-height on all root-to-leaf paths.",
                    "page_number": 1,
                    "section_title": "Invariants & Properties"
                },
                {
                    "text": "Red-Black Tree Height Theorem: Maximum height is at most 2*log2(N+1). Guarantees O(log N) worst-case time complexity for search, insert, and delete operations.",
                    "page_number": 1,
                    "section_title": "Time Complexity"
                }
            ]
        }
    ]

    for note in default_notes:
        chunks = note.pop("chunks")
        cursor.execute("""
        INSERT INTO notes (
            id, user_id, title, subject, subject_badge, format,
            file_type, body, word_count, reading_time_min, chunk_count,
            status, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            note["id"], note["user_id"], note["title"], note["subject"],
            note["subject_badge"], note["format"], note["file_type"],
            note["body"], note["word_count"], note["reading_time_min"],
            note["chunk_count"], note["status"], now, now
        ))

        # Lazy import embedding service to compute vectors for seed chunks
        from backend.services.embedding_service import embedding_service
        for idx, chunk in enumerate(chunks):
            emb = embedding_service.get_embedding(chunk["text"])
            cursor.execute("""
            INSERT INTO note_chunks (
                note_id, user_id, chunk_index, text,
                page_number, section_title, token_count, embedding, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                note["id"], user_id, idx + 1, chunk["text"],
                chunk["page_number"], chunk["section_title"],
                len(chunk["text"].split()), json.dumps(emb), now
            ))

    conn.commit()
    conn.close()


def create_user(
    email: str,
    password: str,
    full_name: str,
    role: str = "student",
    class_grade: Optional[str] = "Class 12 • Senior Secondary",
    target_goal: Optional[str] = "JEE / NEET",
    institution: Optional[str] = "",
    subject: Optional[str] = "",
    bio: Optional[str] = "Passionate STEM student exploring classical mechanics, differential calculus, and organic synthesis.",
    avatar_url: Optional[str] = ""
) -> dict:
    """Creates a new user record and profile in Supabase PostgreSQL & SQLite with salted PBKDF2 hash."""
    email_clean = email.strip().lower()
    full_name_clean = full_name.strip()
    role_clean = role.lower()
    user_id = f"usr_{uuid.uuid4().hex[:12]}"
    prof_id = f"prof_{uuid.uuid4().hex[:12]}"
    pw_hash, salt = hash_password(password)
    now_iso = datetime.utcnow().isoformat()

    # 1. Primary: Write to Supabase PostgreSQL cloud if configured
    try:
        from backend.services.supabase_service import get_pg_connection, is_supabase_configured
        if is_supabase_configured():
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor() as pg_cur:
                    pg_cur.execute("""
                    INSERT INTO users (
                        id, email, password_hash, salt, full_name, role,
                        class_grade, target_goal, institution, subject, bio, avatar_url,
                        created_at, updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                    ON CONFLICT (email) DO UPDATE SET
                        password_hash = EXCLUDED.password_hash,
                        salt = EXCLUDED.salt,
                        full_name = EXCLUDED.full_name,
                        role = EXCLUDED.role,
                        class_grade = EXCLUDED.class_grade,
                        target_goal = EXCLUDED.target_goal,
                        institution = EXCLUDED.institution,
                        subject = EXCLUDED.subject,
                        bio = EXCLUDED.bio,
                        avatar_url = EXCLUDED.avatar_url,
                        updated_at = NOW()
                    RETURNING id;
                    """, (
                        user_id, email_clean, pw_hash, salt, full_name_clean, role_clean,
                        class_grade or "Class 12 • Senior Secondary", target_goal or "JEE / NEET",
                        institution or "", subject or "", bio or "", avatar_url or ""
                    ))
                    res = pg_cur.fetchone()
                    if res and res[0]:
                        user_id = res[0]

                    pg_cur.execute("""
                    INSERT INTO profiles (
                        id, user_id, full_name, email, avatar_url, class_level, preferred_subject,
                        target_goal, institution, bio, created_at, updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                    ON CONFLICT (user_id) DO UPDATE SET
                        full_name = EXCLUDED.full_name,
                        email = EXCLUDED.email,
                        avatar_url = EXCLUDED.avatar_url,
                        class_level = EXCLUDED.class_level,
                        preferred_subject = EXCLUDED.preferred_subject,
                        target_goal = EXCLUDED.target_goal,
                        institution = EXCLUDED.institution,
                        bio = EXCLUDED.bio,
                        updated_at = NOW()
                    """, (
                        prof_id, user_id, full_name_clean, email_clean, avatar_url or "",
                        class_grade or "Class 12 • Senior Secondary", subject or "Physics",
                        target_goal or "JEE / NEET", institution or "", bio or ""
                    ))
                    pg_conn.commit()
    except Exception as pg_err:
        print(f"[Supabase Cloud Sync] create_user warning: {pg_err}")

    # 2. Local SQLite synchronization (for dev & offline fallback)
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE LOWER(email) = ?", (email_clean,))
        existing_sqlite = cursor.fetchone()
        if existing_sqlite:
            user_id = existing_sqlite[0]
            cursor.execute("""
            UPDATE users SET
                password_hash = ?, salt = ?, full_name = ?, role = ?,
                class_grade = ?, target_goal = ?, institution = ?, subject = ?, bio = ?, avatar_url = ?,
                updated_at = ?
            WHERE id = ?
            """, (
                pw_hash, salt, full_name_clean, role_clean,
                class_grade or "Class 12 • Senior Secondary", target_goal or "JEE / NEET",
                institution or "", subject or "", bio or "", avatar_url or "",
                now_iso, user_id
            ))
        else:
            cursor.execute("""
            INSERT INTO users (
                id, email, password_hash, salt, full_name, role,
                class_grade, target_goal, institution, subject, bio, avatar_url,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, email_clean, pw_hash, salt, full_name_clean, role_clean,
                class_grade or "Class 12 • Senior Secondary", target_goal or "JEE / NEET",
                institution or "", subject or "", bio or "", avatar_url or "",
                now_iso, now_iso
            ))

        cursor.execute("""
        INSERT INTO profiles (
            id, user_id, full_name, email, avatar_url, class_level, preferred_subject,
            target_goal, institution, bio, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            full_name = excluded.full_name,
            email = excluded.email,
            avatar_url = excluded.avatar_url,
            class_level = excluded.class_level,
            preferred_subject = excluded.preferred_subject,
            target_goal = excluded.target_goal,
            institution = excluded.institution,
            bio = excluded.bio,
            updated_at = excluded.updated_at
        """, (
            prof_id, user_id, full_name_clean, email_clean, avatar_url or "",
            class_grade or "Class 12 • Senior Secondary", subject or "Physics",
            target_goal or "JEE / NEET", institution or "", bio or "",
            now_iso, now_iso
        ))
        conn.commit()
        conn.close()
    except Exception as sqlite_err:
        print(f"[SQLite Sync] create_user warning: {sqlite_err}")

    # Initialize user telemetry
    try:
        get_or_create_user_telemetry(user_id)
    except Exception:
        pass

    # Seed initial curriculum notes
    try:
        seed_default_notes_for_user(user_id)
    except Exception:
        pass

    return get_user_by_id(user_id)


def update_user_role(user_id: str, new_role: str) -> Optional[dict]:
    """Updates user role across Supabase Cloud PostgreSQL and local SQLite."""
    role_clean = new_role.strip().lower()
    now_iso = datetime.utcnow().isoformat()

    # 1. Supabase PostgreSQL
    try:
        from backend.services.supabase_service import get_pg_connection, is_supabase_configured
        if is_supabase_configured():
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor() as pg_cur:
                    pg_cur.execute(
                        "UPDATE public.users SET role = %s, updated_at = NOW() WHERE id = %s;",
                        (role_clean, user_id)
                    )
                    pg_conn.commit()
    except Exception as pg_err:
        print(f"[Supabase Cloud Sync] update_user_role warning: {pg_err}")

    # 2. SQLite
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET role = ?, updated_at = ? WHERE id = ?;", (role_clean, now_iso, user_id))
        conn.commit()
        conn.close()
    except Exception as sqlite_err:
        print(f"[SQLite Sync] update_user_role warning: {sqlite_err}")

    return get_user_by_id(user_id)


def get_user_by_email(email: str) -> Optional[dict]:
    """Fetches user record by email from Supabase Cloud PostgreSQL or local SQLite."""
    if not email:
        return None
    email_clean = email.strip().lower()

    # 1. Check Supabase Cloud PostgreSQL
    try:
        from backend.services.supabase_service import get_pg_connection, is_supabase_configured
        from psycopg2.extras import RealDictCursor
        if is_supabase_configured():
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor(cursor_factory=RealDictCursor) as pg_cur:
                    pg_cur.execute("SELECT * FROM users WHERE email = %s LIMIT 1", (email_clean,))
                    row = pg_cur.fetchone()
                    if row:
                        return dict(row)
    except Exception as err:
        print(f"[Supabase Cloud Sync] get_user_by_email warning: {err}")

    # 2. Local SQLite fallback
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE LOWER(email) = ?", (email_clean,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return dict(row)
    except Exception:
        pass
    return None


def get_user_by_id(user_id: str) -> Optional[dict]:
    """Fetches user record by user_id from Supabase Cloud PostgreSQL or local SQLite."""
    if not user_id:
        return None
    user_id_clean = user_id.strip()

    # 1. Check Supabase Cloud PostgreSQL
    try:
        from backend.services.supabase_service import get_pg_connection, is_supabase_configured
        from psycopg2.extras import RealDictCursor
        if is_supabase_configured():
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor(cursor_factory=RealDictCursor) as pg_cur:
                    pg_cur.execute("SELECT * FROM users WHERE id = %s LIMIT 1", (user_id_clean,))
                    row = pg_cur.fetchone()
                    if row:
                        return dict(row)
    except Exception as err:
        print(f"[Supabase Cloud Sync] get_user_by_id warning: {err}")

    # 2. Local SQLite fallback
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id_clean,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return dict(row)
    except Exception:
        pass
    return None


def get_or_create_profile(user_id: str) -> dict:
    """Retrieves or auto-creates a student profile record from Cloud PostgreSQL or SQLite."""
    if not user_id:
        return {}

    # 1. Check Cloud PostgreSQL
    try:
        from backend.services.supabase_service import get_pg_connection, is_supabase_configured
        from psycopg2.extras import RealDictCursor
        if is_supabase_configured():
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor(cursor_factory=RealDictCursor) as pg_cur:
                    pg_cur.execute("SELECT * FROM profiles WHERE user_id = %s LIMIT 1", (user_id,))
                    prof = pg_cur.fetchone()
                    if prof:
                        return dict(prof)

                    pg_cur.execute("SELECT * FROM users WHERE id = %s LIMIT 1", (user_id,))
                    u = pg_cur.fetchone()
                    if u:
                        prof_id = f"prof_{uuid.uuid4().hex[:12]}"
                        pg_cur.execute("""
                        INSERT INTO profiles (
                            id, user_id, full_name, email, avatar_url, class_level, preferred_subject,
                            target_goal, institution, bio, created_at, updated_at
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                        ON CONFLICT (user_id) DO NOTHING
                        """, (
                            prof_id, user_id, u["full_name"], u["email"], u.get("avatar_url", "") or "",
                            u.get("class_grade", "Class 12 • Senior Secondary") or "Class 12 • Senior Secondary",
                            u.get("subject", "Physics") or "Physics",
                            u.get("target_goal", "JEE / NEET") or "JEE / NEET",
                            u.get("institution", "") or "",
                            u.get("bio", "") or ""
                        ))
                        pg_conn.commit()
                        pg_cur.execute("SELECT * FROM profiles WHERE user_id = %s LIMIT 1", (user_id,))
                        new_prof = pg_cur.fetchone()
                        if new_prof:
                            return dict(new_prof)
    except Exception as err:
        print(f"[Supabase Cloud Sync] get_or_create_profile warning: {err}")

    # 2. Local SQLite fallback
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            profile = dict(row)
            conn.close()
            return profile

        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return {}

        now = datetime.utcnow().isoformat()
        prof_id = f"prof_{uuid.uuid4().hex[:12]}"
        cursor.execute("""
        INSERT OR REPLACE INTO profiles (
            id, user_id, full_name, email, avatar_url, class_level, preferred_subject,
            target_goal, institution, bio, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            prof_id, user_id, user["full_name"], user["email"], user["avatar_url"],
            user["class_grade"] or "Class 12 • Senior Secondary",
            user["subject"] or "Physics",
            user["target_goal"] or "JEE / NEET",
            user["institution"] or "",
            user["bio"] or "",
            now, now
        ))
        conn.commit()
        cursor.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,))
        prof_row = cursor.fetchone()
        conn.close()
        return dict(prof_row) if prof_row else {}
    except Exception:
        return {}


def update_user_profile(user_id: str, **kwargs) -> Optional[dict]:
    """Updates user profile fields dynamically across PostgreSQL and SQLite."""
    allowed_fields = ["full_name", "class_grade", "target_goal", "institution", "subject", "bio", "avatar_url"]

    # 1. Update Cloud PostgreSQL
    try:
        from backend.services.supabase_service import get_pg_connection, is_supabase_configured
        if is_supabase_configured():
            pg_updates = []
            pg_values = []
            for field in allowed_fields:
                if field in kwargs and kwargs[field] is not None:
                    pg_updates.append(f"{field} = %s")
                    pg_values.append(kwargs[field])
            if pg_updates:
                pg_updates.append("updated_at = NOW()")
                pg_values.append(user_id)
                with get_pg_connection() as pg_conn:
                    with pg_conn.cursor() as pg_cur:
                        pg_cur.execute(f"UPDATE users SET {', '.join(pg_updates)} WHERE id = %s", tuple(pg_values))

                        prof_field_map = {
                            "full_name": "full_name", "class_grade": "class_level",
                            "target_goal": "target_goal", "institution": "institution",
                            "subject": "preferred_subject", "bio": "bio", "avatar_url": "avatar_url"
                        }
                        prof_up = []
                        prof_val = []
                        for k, v in kwargs.items():
                            if k in prof_field_map and v is not None:
                                prof_up.append(f"{prof_field_map[k]} = %s")
                                prof_val.append(v)
                        if prof_up:
                            prof_up.append("updated_at = NOW()")
                            prof_val.append(user_id)
                            pg_cur.execute(f"UPDATE profiles SET {', '.join(prof_up)} WHERE user_id = %s", tuple(prof_val))
                        pg_conn.commit()
    except Exception as err:
        print(f"[Supabase Cloud Sync] update_user_profile warning: {err}")

    # 2. Update SQLite
    try:
        updates = []
        values = []
        for field in allowed_fields:
            if field in kwargs and kwargs[field] is not None:
                updates.append(f"{field} = ?")
                values.append(kwargs[field])
        if updates:
            now = datetime.utcnow().isoformat()
            updates.append("updated_at = ?")
            values.append(now)
            values.append(user_id)
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(f"UPDATE users SET {', '.join(updates)} WHERE id = ?", tuple(values))

            prof_field_map = {
                "full_name": "full_name", "class_grade": "class_level",
                "target_goal": "target_goal", "institution": "institution",
                "subject": "preferred_subject", "bio": "bio", "avatar_url": "avatar_url"
            }
            prof_updates = []
            prof_values = []
            for k, v in kwargs.items():
                if k in prof_field_map and v is not None:
                    prof_updates.append(f"{prof_field_map[k]} = ?")
                    prof_values.append(v)
            if prof_updates:
                prof_updates.append("updated_at = ?")
                prof_values.append(now)
                prof_values.append(user_id)
                cursor.execute(f"UPDATE profiles SET {', '.join(prof_updates)} WHERE user_id = ?", tuple(prof_values))
            conn.commit()
            conn.close()
    except Exception:
        pass

    return get_or_create_profile(user_id)


def create_session(user_id: str, expire_days: int = 7) -> str:
    """Generates and stores a secure session token in Supabase PostgreSQL and local SQLite."""
    token = f"siksha_sess_{secrets.token_hex(24)}"
    now = datetime.utcnow()
    expires_at = (now + timedelta(days=expire_days)).isoformat()

    # 1. Supabase Cloud PostgreSQL
    try:
        from backend.services.supabase_service import get_pg_connection, is_supabase_configured
        if is_supabase_configured():
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor() as pg_cur:
                    # Check if user exists in Supabase users table
                    pg_cur.execute("SELECT id FROM users WHERE id = %s LIMIT 1", (user_id,))
                    if not pg_cur.fetchone():
                        # Fetch user details from SQLite to sync to Supabase
                        try:
                            s_conn = get_db_connection()
                            s_cur = s_conn.cursor()
                            s_cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
                            sqlite_u = s_cur.fetchone()
                            s_conn.close()
                            if sqlite_u:
                                u_dict = dict(sqlite_u)
                                pg_cur.execute("""
                                INSERT INTO users (
                                    id, email, password_hash, salt, full_name, role,
                                    class_grade, target_goal, institution, subject, bio, avatar_url,
                                    created_at, updated_at
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                                ON CONFLICT (email) DO UPDATE SET
                                    full_name = EXCLUDED.full_name,
                                    updated_at = NOW()
                                """, (
                                    u_dict["id"], u_dict["email"], u_dict["password_hash"], u_dict["salt"],
                                    u_dict.get("full_name", "Student"), u_dict.get("role", "student"),
                                    u_dict.get("class_grade", "Class 12 • Senior Secondary"),
                                    u_dict.get("target_goal", "JEE / NEET"),
                                    u_dict.get("institution", ""), u_dict.get("subject", ""),
                                    u_dict.get("bio", ""), u_dict.get("avatar_url", "")
                                ))
                        except Exception as sync_e:
                            print(f"[Supabase Cloud Sync] User auto-sync in create_session warning: {sync_e}")

                    pg_cur.execute("""
                    INSERT INTO user_sessions (token, user_id, expires_at, created_at)
                    VALUES (%s, %s, NOW() + INTERVAL '7 days', NOW())
                    ON CONFLICT (token) DO UPDATE SET
                        expires_at = EXCLUDED.expires_at
                    """, (token, user_id))
                    pg_conn.commit()
    except Exception as err:
        print(f"[Supabase Cloud Sync] create_session warning: {err}")

    # 2. Local SQLite fallback
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO user_sessions (token, user_id, expires_at, created_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(token) DO UPDATE SET expires_at = excluded.expires_at
        """, (token, user_id, expires_at, now.isoformat()))
        conn.commit()
        conn.close()
    except Exception as sqlite_sess_err:
        print(f"[SQLite Sync] create_session warning: {sqlite_sess_err}")

    return token


def get_user_from_session(token: Any) -> Optional[dict]:
    """Validates session token (Supabase JWT, Cloud PostgreSQL session, or SQLite session) and returns associated user dict."""
    if not token or not isinstance(token, str):
        return None
    token = token.strip()
    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "").strip()

    # 0. Check in-memory session cache (instant 0ms response)
    try:
        from backend.services.supabase_service import get_cached_session_user, set_cached_session_user
        cached_user = get_cached_session_user(token)
        if cached_user:
            return cached_user
    except Exception:
        pass

    # 1. Authentic Supabase JWTs start with 'ey' and contain 2 dots
    if token.startswith("ey") and token.count(".") == 2:
        try:
            from backend.services.supabase_service import verify_supabase_token, is_supabase_configured
            if is_supabase_configured():
                sb_user = verify_supabase_token(token)
                if sb_user:
                    user = get_user_by_id(sb_user["id"])
                    if not user:
                        user = create_user(
                            email=sb_user.get("email", ""),
                            password=secrets.token_urlsafe(16),
                            full_name=sb_user.get("full_name", "Student"),
                            role=sb_user.get("role", "student"),
                            class_grade=sb_user.get("class_grade", "Class 12 • Senior Secondary"),
                            target_goal=sb_user.get("target_goal", "JEE / NEET")
                        )
                    resolved = user or sb_user
                    try:
                        set_cached_session_user(token, resolved)
                    except Exception:
                        pass
                    return resolved
        except Exception:
            pass

    # 2. Supabase Cloud PostgreSQL user_sessions JOIN users lookup in 1 single round trip
    try:
        from backend.services.supabase_service import get_pg_connection, is_supabase_configured
        from psycopg2.extras import RealDictCursor
        if is_supabase_configured():
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor(cursor_factory=RealDictCursor) as pg_cur:
                    pg_cur.execute("""
                    SELECT u.*, s.expires_at AS session_expires_at
                    FROM users u
                    JOIN user_sessions s ON u.id = s.user_id
                    WHERE s.token = %s AND s.expires_at > NOW()
                    LIMIT 1
                    """, (token,))
                    session_row = pg_cur.fetchone()
                    if session_row:
                        user_dict = dict(session_row)
                        try:
                            set_cached_session_user(token, user_dict)
                        except Exception:
                            pass
                        return user_dict
    except Exception as err:
        print(f"[Supabase Cloud Sync] get_user_from_session warning: {err}")

    # 3. Local SQLite sessions fallback
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT u.*, s.expires_at AS session_expires_at
        FROM users u
        JOIN user_sessions s ON u.id = s.user_id
        WHERE s.token = ?
        LIMIT 1
        """, (token,))
        row = cursor.fetchone()
        conn.close()

        if row:
            user_dict = dict(row)
            expires_at_str = user_dict.get("session_expires_at")
            if expires_at_str:
                try:
                    expires_at = datetime.fromisoformat(expires_at_str)
                    if datetime.utcnow() > expires_at:
                        return None
                except Exception:
                    pass
            try:
                set_cached_session_user(token, user_dict)
            except Exception:
                pass
            return user_dict
    except Exception:
        pass

    return None


def delete_session(token: Any):
    """Removes a session token upon user logout."""
    if not token or not isinstance(token, str):
        return
    token_clean = token.replace("Bearer ", "").strip()

    try:
        from backend.services.supabase_service import invalidate_session_cache
        invalidate_session_cache(token_clean)
    except Exception:
        pass

    # Cloud PostgreSQL
    try:
        from backend.services.supabase_service import get_pg_connection, is_supabase_configured
        if is_supabase_configured():
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor() as pg_cur:
                    pg_cur.execute("DELETE FROM user_sessions WHERE token = %s", (token,))
                    pg_conn.commit()
    except Exception:
        pass

    # SQLite
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_sessions WHERE token = ?", (token,))
        conn.commit()
        conn.close()
    except Exception:
        pass



def get_or_create_user_telemetry(user_id: str) -> dict:
    """Retrieves student learning telemetry from Cloud PostgreSQL or SQLite, creating default baseline if not yet present."""
    default_subjects = {
        "Physics": 0.0,
        "Mathematics": 0.0,
        "Chemistry": 0.0,
        "Computer Science": 0.0
    }
    default_frontier = []
    now = datetime.utcnow().isoformat()

    # 1. Cloud PostgreSQL (Supabase)
    try:
        from backend.services.supabase_service import get_pg_connection, is_supabase_configured
        from psycopg2.extras import RealDictCursor
        if is_supabase_configured():
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor(cursor_factory=RealDictCursor) as pg_cur:
                    pg_cur.execute("SELECT * FROM public.user_telemetry WHERE user_id = %s LIMIT 1", (user_id,))
                    row = pg_cur.fetchone()
                    if row:
                        data = dict(row)
                        sm = data.get("subject_mastery_json")
                        kf = data.get("knowledge_frontier_json")
                        data["subject_mastery"] = json.loads(sm) if isinstance(sm, str) else (sm or default_subjects)
                        data["knowledge_frontier"] = json.loads(kf) if isinstance(kf, str) else (kf or default_frontier)
                        return data

                    # Calculate initial telemetry from any existing quiz attempts if available
                    pg_cur.execute("SELECT COUNT(*), AVG(accuracy_percent) FROM public.quiz_attempts WHERE user_id = %s", (user_id,))
                    att_row = pg_cur.fetchone()
                    tot_solved = 0
                    init_mastery = 0.0
                    if att_row and att_row["count"] > 0:
                        tot_solved = att_row["count"] * 10
                        init_mastery = round(float(att_row["avg"] or 0.0), 1)

                    pg_cur.execute("""
                    INSERT INTO public.user_telemetry (
                        user_id, overall_mastery_percent, active_learning_streak_days,
                        questions_solved, socratic_dialogues_count, subject_mastery_json,
                        knowledge_frontier_json, updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
                    ON CONFLICT (user_id) DO UPDATE SET updated_at = NOW()
                    RETURNING *;
                    """, (
                        user_id, init_mastery, 0, tot_solved, 0,
                        json.dumps(default_subjects), json.dumps(default_frontier)
                    ))
                    pg_conn.commit()
                    new_row = pg_cur.fetchone()
                    if new_row:
                        data = dict(new_row)
                        data["subject_mastery"] = default_subjects
                        data["knowledge_frontier"] = default_frontier
                        return data
    except Exception as err:
        logger.warning(f"[Supabase Cloud Sync] get_or_create_user_telemetry warning: {err}")

    # 2. Local SQLite fallback
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_telemetry WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()

        if row:
            conn.close()
            data = dict(row)
            sm = data.get("subject_mastery_json")
            kf = data.get("knowledge_frontier_json")
            data["subject_mastery"] = json.loads(sm) if isinstance(sm, str) else (sm or default_subjects)
            data["knowledge_frontier"] = json.loads(kf) if isinstance(kf, str) else (kf or default_frontier)
            return data

        # Safe insert: check if user exists in SQLite users table first to avoid FK constraint failure
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if cursor.fetchone():
            cursor.execute("""
            INSERT OR IGNORE INTO user_telemetry (
                user_id, overall_mastery_percent, active_learning_streak_days,
                questions_solved, socratic_dialogues_count, subject_mastery_json,
                knowledge_frontier_json, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, 0.0, 0, 0, 0,
                json.dumps(default_subjects), json.dumps(default_frontier), now
            ))
            conn.commit()
        conn.close()
    except Exception as err:
        logger.warning(f"[SQLite] get_or_create_user_telemetry warning: {err}")

    return {
        "user_id": user_id,
        "overall_mastery_percent": 0.0,
        "active_learning_streak_days": 0,
        "questions_solved": 0,
        "socratic_dialogues_count": 0,
        "subject_mastery": default_subjects,
        "knowledge_frontier": default_frontier,
        "updated_at": now
    }


def update_user_telemetry(
    user_id: str,
    solved_increment: int = 0,
    mastery_delta: float = 0.0,
    socratic_increment: int = 0
) -> dict:
    """Updates telemetry metrics (e.g. after solving practice problems or socratic inquiry)."""
    if user_id == "usr_demo_sandbox" or user_id.startswith("usr_demo"):
        return {
            "user_id": user_id,
            "questions_solved": solved_increment,
            "socratic_dialogues_count": socratic_increment,
            "overall_mastery_percent": 50.0,
            "active_learning_streak_days": 1,
            "subject_mastery": {},
            "knowledge_frontier": {},
            "is_demo": True
        }

    telemetry = get_or_create_user_telemetry(user_id)
    new_solved = telemetry["questions_solved"] + solved_increment
    new_socratic = telemetry["socratic_dialogues_count"] + socratic_increment
    new_mastery = max(10.0, min(99.9, round(telemetry["overall_mastery_percent"] + mastery_delta, 1)))
    now = datetime.utcnow().isoformat()

    # 1. Update Cloud PostgreSQL
    try:
        from backend.services.supabase_service import get_pg_connection, is_supabase_configured
        if is_supabase_configured():
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor() as pg_cur:
                    pg_cur.execute("""
                    UPDATE public.user_telemetry
                    SET questions_solved = %s, socratic_dialogues_count = %s, overall_mastery_percent = %s, updated_at = NOW()
                    WHERE user_id = %s
                    """, (new_solved, new_socratic, new_mastery, user_id))
                    pg_conn.commit()
    except Exception as err:
        logger.warning(f"[Supabase] update_user_telemetry warning: {err}")

    # 2. Update SQLite
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE user_telemetry
        SET questions_solved = ?, socratic_dialogues_count = ?, overall_mastery_percent = ?, updated_at = ?
        WHERE user_id = ?
        """, (new_solved, new_socratic, new_mastery, now, user_id))
        conn.commit()
        conn.close()
    except Exception:
        pass

    telemetry["questions_solved"] = new_solved
    telemetry["socratic_dialogues_count"] = new_socratic
    telemetry["overall_mastery_percent"] = new_mastery
    telemetry["updated_at"] = now
    return telemetry


def seed_default_users():
    """Ensures standard default accounts exist in SQLite DB."""
    defaults = [
        {
            "email": "aarav@siksha.edu",
            "password": "student123",
            "full_name": "Aarav Sharma",
            "role": "student",
            "class_grade": "Class 12 • Senior Secondary",
            "target_goal": "JEE Advanced 2027 & CBSE 12",
            "bio": "Passionate STEM student exploring classical mechanics, differential calculus, and organic synthesis. Aiming for Top 500 rank in JEE Advanced 2027.",
            "institution": "Delhi Public School, R.K. Puram"
        },
        {
            "email": "student2@siksha.edu",
            "password": "student123",
            "full_name": "Diya Patel",
            "role": "student",
            "class_grade": "Class 12 • Science",
            "target_goal": "NEET 2027 & CBSE 12",
            "bio": "Curious learner exploring organic chemistry, cell biology, and genetics.",
            "institution": "Delhi Public School, R.K. Puram"
        },
        {
            "email": "demo@student.com",
            "password": "password",
            "full_name": "Demo Student",
            "role": "student",
            "class_grade": "Class 12 • Science",
            "target_goal": "JEE / NEET",
            "bio": "Curious learner exploring physics, mathematics, and computing.",
            "institution": "SikshaSaathi Academy"
        },
        {
            "email": "teacher@siksha.edu",
            "password": "teacher123",
            "full_name": "Dr. Rajesh Verma",
            "role": "teacher",
            "class_grade": "Faculty • Senior Secondary",
            "target_goal": "Curriculum Diagnostic Lead",
            "bio": "Senior Physics Educator guiding students with deep conceptual intuition.",
            "institution": "Delhi Public School, R.K. Puram",
            "subject": "Physics"
        },
        {
            "email": "teacher2@siksha.edu",
            "password": "teacher123",
            "full_name": "Dr. Priya Nair",
            "role": "teacher",
            "class_grade": "Faculty • Senior Secondary",
            "target_goal": "Head of Science • Educator",
            "bio": "Senior Chemistry Educator specializing in organic mechanisms and classroom diagnostics.",
            "institution": "National Science Academy",
            "subject": "Chemistry"
        }
    ]

    for user_info in defaults:
        existing = get_user_by_email(user_info["email"])
        if not existing:
            create_user(**user_info)

    # Seed default classroom and enrollment for immediate verification
    teacher = get_user_by_email("teacher@siksha.edu")
    student = get_user_by_email("aarav@siksha.edu")
    if teacher and student:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM classrooms WHERE join_code = 'PHY-1201'")
        row = cursor.fetchone()
        now = datetime.utcnow().isoformat()
        if not row:
            class_id = f"cls_{uuid.uuid4().hex[:12]}"
            cursor.execute("""
            INSERT INTO classrooms (id, teacher_id, name, subject, grade_level, description, join_code, is_active, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
            """, (
                class_id, teacher["id"], "Class 12-A • Physics & STEM Cohort", "Physics",
                "Class 12 • Senior Secondary", "Senior secondary physics, mechanics, and electromagnetism cohort.",
                "PHY-1201", now, now
            ))
            cursor.execute("""
            INSERT OR IGNORE INTO classroom_members (classroom_id, student_id, joined_at, status)
            VALUES (?, ?, ?, 'active')
            """, (class_id, student["id"], now))
            conn.commit()
        conn.close()


def seed_practice_data():
    """Seeds the 5 subjects, 5 levels each, and 250 questions into SQLite if not already populated."""
    from backend.data.question_bank import SUBJECTS_DATA, LEVELS_DATA, QUESTIONS_DATA

    conn = get_db_connection()
    cursor = conn.cursor()

    for subj in SUBJECTS_DATA:
        cursor.execute("SELECT COUNT(*) FROM practice_subjects WHERE id = ?", (subj["id"],))
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO practice_subjects (id, title, description, icon, order_index) VALUES (?, ?, ?, ?, ?)",
                (subj["id"], subj["title"], subj["description"], subj["icon"], subj["order_index"])
            )

    for subj in SUBJECTS_DATA:
        for lvl in LEVELS_DATA:
            level_id = f"{subj['id']}_lvl_{lvl['level_number']}"
            cursor.execute("SELECT COUNT(*) FROM practice_levels WHERE id = ?", (level_id,))
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    "INSERT INTO practice_levels (id, subject_id, level_number, title, description, question_count, order_index) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (level_id, subj["id"], lvl["level_number"], lvl["title"], lvl["description"], lvl["question_count"], lvl["level_number"])
                )

    for q in QUESTIONS_DATA:
        cursor.execute("SELECT COUNT(*) FROM practice_questions WHERE id = ?", (q["id"],))
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
            INSERT INTO practice_questions (
                id, subject_id, level_number, order_index, topic, difficulty,
                question_text, option_a, option_b, option_c, option_d, correct_option, explanation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                q["id"], q["subject_id"], q["level_number"], q["order_index"],
                q["topic"], q["difficulty"], q["question_text"],
                q["option_a"], q["option_b"], q["option_c"], q["option_d"],
                q["correct_option"], q["explanation"]
            ))

    conn.commit()
    conn.close()


def get_practice_subjects(user_id: str) -> list[dict]:
    """Returns the 4 practice subjects with dynamically computed level completion and progress."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM practice_subjects ORDER BY order_index ASC")
    subjects = [dict(r) for r in cursor.fetchall()]

    for subj in subjects:
        s_id = subj["id"]
        cursor.execute("""
        SELECT DISTINCT level_number, MAX(score) as best_score, MAX(accuracy_percent) as best_accuracy
        FROM quiz_attempts
        WHERE user_id = ? AND subject_id = ?
        GROUP BY level_number
        """, (user_id, s_id))
        completed_rows = cursor.fetchall()
        completed_levels = len(completed_rows)
        subj["completed_levels"] = completed_levels
        subj["total_levels"] = 5
        subj["progress_percent"] = round((completed_levels / 5.0) * 100, 1)
        subj["unlocked_level"] = min(completed_levels + 1, 5)

        if completed_rows:
            avg_acc = sum(r["best_accuracy"] for r in completed_rows) / len(completed_rows)
            subj["accuracy_percent"] = round(avg_acc, 1)
        else:
            subj["accuracy_percent"] = 0.0

    conn.close()
    return subjects


def get_practice_subject_levels(subject_id: str, user_id: str) -> list[dict]:
    """Returns the 5 levels for a subject with unlocking rules and user's best scores."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM practice_levels WHERE subject_id = ? ORDER BY level_number ASC", (subject_id,))
    levels = [dict(r) for r in cursor.fetchall()]

    cursor.execute("""
    SELECT level_number, COUNT(*) as attempts_count, MAX(score) as best_score, MAX(accuracy_percent) as best_accuracy, MAX(completed_at) as last_completed_at
    FROM quiz_attempts
    WHERE user_id = ? AND subject_id = ?
    GROUP BY level_number
    """, (user_id, subject_id))
    attempts_map = {r["level_number"]: dict(r) for r in cursor.fetchall()}
    conn.close()

    completed_so_far = True
    for lvl in levels:
        num = lvl["level_number"]
        att = attempts_map.get(num)
        if att and att["attempts_count"] > 0:
            lvl["status"] = "completed"
            lvl["best_score"] = att["best_score"]
            lvl["best_accuracy"] = round(att["best_accuracy"], 1)
            lvl["attempts_count"] = att["attempts_count"]
            lvl["last_completed_at"] = att["last_completed_at"]
        else:
            if num == 1 or completed_so_far:
                lvl["status"] = "unlocked"
            else:
                lvl["status"] = "locked"
            lvl["best_score"] = 0
            lvl["best_accuracy"] = 0.0
            lvl["attempts_count"] = 0
            lvl["last_completed_at"] = None
            completed_so_far = False

    return levels


def get_practice_level_questions(subject_id: str, level_number: int, sanitize: bool = True) -> list[dict]:
    """Fetches questions for a specific subject level, supporting dynamic pools and option randomization."""
    import random
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM practice_questions
    WHERE subject_id = ? AND level_number = ?
    ORDER BY order_index ASC
    """, (subject_id, level_number))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()

    if not rows:
        return []

    # Pick up to 10 questions, shuffling order for variety
    selected_rows = list(rows)
    if len(selected_rows) > 10:
        selected_rows = random.sample(selected_rows, 10)
    else:
        random.shuffle(selected_rows)

    questions = []
    for r in selected_rows:
        q = {
            "id": r["id"],
            "subject_id": r["subject_id"],
            "level_number": r["level_number"],
            "order_index": r["order_index"],
            "topic": r["topic"],
            "difficulty": r["difficulty"],
            "question_text": r["question_text"],
            "option_a": r["option_a"],
            "option_b": r["option_b"],
            "option_c": r["option_c"],
            "option_d": r["option_d"]
        }
        if not sanitize:
            q["correct_option"] = r["correct_option"]
            q["explanation"] = r["explanation"]
        questions.append(q)

    return questions


def submit_quiz_attempt(
    user_id: str,
    subject_id: str,
    level_number: int,
    answers: list[dict],
    time_spent_seconds: int = 0
) -> dict:
    """Evaluates quiz server-side within an atomic transaction, records attempt and answers in SQLite."""
    import uuid
    attempt_id = f"att_{uuid.uuid4().hex[:12]}"
    now = datetime.utcnow().isoformat()

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Load master questions for validation by ID first, then fallback to level
        q_ids = [a["question_id"] for a in answers if isinstance(a, dict) and "question_id" in a]
        master_questions = {}
        if q_ids:
            placeholders = ",".join(["?"] * len(q_ids))
            cursor.execute(f"""
            SELECT id, question_text, option_a, option_b, option_c, option_d, correct_option, explanation, topic
            FROM practice_questions
            WHERE id IN ({placeholders})
            """, q_ids)
            master_questions = {r["id"]: dict(r) for r in cursor.fetchall()}

        if not master_questions:
            cursor.execute("""
            SELECT id, question_text, option_a, option_b, option_c, option_d, correct_option, explanation, topic
            FROM practice_questions
            WHERE subject_id = ? AND level_number = ?
            ORDER BY order_index ASC
            """, (subject_id, level_number))
            master_questions = {r["id"]: dict(r) for r in cursor.fetchall()}

        if not master_questions:
            raise ValueError(f"No master questions found for {subject_id} Level {level_number}")

        score = 0
        total_questions = len(master_questions)
        answers_review = []

        user_ans_map = {}
        for a in answers:
            if isinstance(a, dict) and "question_id" in a:
                user_ans_map[a["question_id"]] = a.get("selected_option", -1)

        # Preserve exact question sequence from the student's submission
        ordered_q_ids = []
        for a in answers:
            if isinstance(a, dict) and "question_id" in a:
                qid = a["question_id"]
                if qid in master_questions and qid not in ordered_q_ids:
                    ordered_q_ids.append(qid)
        for qid in master_questions:
            if qid not in ordered_q_ids:
                ordered_q_ids.append(qid)

        answers_to_insert = []
        for q_id in ordered_q_ids:
            q_data = master_questions[q_id]
            raw_user_choice = user_ans_map.get(q_id, -1)
            try:
                user_choice = int(raw_user_choice) if raw_user_choice is not None else -1
            except (ValueError, TypeError):
                user_choice = -1

            try:
                correct_choice = int(q_data["correct_option"])
            except (ValueError, TypeError):
                correct_choice = 0

            is_correct = 1 if (user_choice == correct_choice and user_choice >= 0) else 0
            if is_correct:
                score += 1

            answers_to_insert.append((attempt_id, user_id, q_id, user_choice, correct_choice, is_correct))

            options = [q_data["option_a"], q_data["option_b"], q_data["option_c"], q_data["option_d"]]
            answers_review.append({
                "question_id": q_id,
                "question_text": q_data["question_text"],
                "options": options,
                "selected_option": user_choice,
                "correct_option": correct_choice,
                "is_correct": bool(is_correct),
                "explanation": q_data["explanation"],
                "topic": q_data["topic"]
            })

        accuracy_percent = round((score / max(total_questions, 1)) * 100.0, 1)

        if user_id == "usr_demo_sandbox" or user_id.startswith("usr_demo"):
            conn.close()
            next_level = min(level_number + 1, 5)
            return {
                "attempt_id": attempt_id,
                "subject_id": subject_id,
                "level_number": level_number,
                "score": score,
                "total_questions": total_questions,
                "accuracy_percent": accuracy_percent,
                "time_spent_seconds": time_spent_seconds,
                "is_unlocked_next": (level_number < 5),
                "next_level_number": next_level,
                "answers_review": answers_review,
                "completed_at": now,
                "is_demo": True
            }

        # Ensure user exists in users table before inserting attempt
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        sqlite_user = cursor.fetchone()
        real_user = dict(sqlite_user) if sqlite_user else get_user_by_id(user_id)
        if real_user and not sqlite_user:
            cursor.execute("""
            INSERT OR IGNORE INTO users (id, email, password_hash, salt, full_name, role, class_grade, target_goal, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
            """, (
                real_user["id"], real_user.get("email", f"{user_id}@student.siksha.edu"),
                real_user.get("password_hash", ""), real_user.get("salt", ""),
                real_user.get("full_name", "Student"), real_user.get("role", "student"),
                real_user.get("class_grade", "Class 12"), real_user.get("target_goal", "JEE / NEET")
            ))

        # Insert parent attempt record first
        cursor.execute("""
        INSERT INTO quiz_attempts (
            id, user_id, subject_id, level_number, score, total_questions, accuracy_percent, time_spent_seconds, completed_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (attempt_id, user_id, subject_id, level_number, score, total_questions, accuracy_percent, time_spent_seconds, now))

        # Insert child answer records
        for ans_row in answers_to_insert:
            cursor.execute("""
            INSERT INTO quiz_answers (
                attempt_id, user_id, question_id, selected_option, correct_option, is_correct
            ) VALUES (?, ?, ?, ?, ?, ?)
            """, ans_row)

        conn.commit()

        # Also persist to Supabase PostgreSQL in real-time if configured
        try:
            from backend.services.supabase_service import get_pg_connection, is_supabase_configured
            if is_supabase_configured():
                with get_pg_connection() as pg_conn:
                    pg_cur = pg_conn.cursor()
                    if real_user:
                        pg_cur.execute("""
                        INSERT INTO public.users (id, email, password_hash, salt, full_name, role, class_grade, target_goal, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                        ON CONFLICT (email) DO NOTHING;
                        """, (
                            real_user["id"], real_user.get("email", f"{user_id}@student.siksha.edu"),
                            real_user.get("password_hash", ""), real_user.get("salt", ""),
                            real_user.get("full_name", "Student"), real_user.get("role", "student"),
                            real_user.get("class_grade", "Class 12"), real_user.get("target_goal", "JEE / NEET")
                        ))
                    
                    pg_cur.execute("""
                    INSERT INTO public.quiz_attempts (id, user_id, subject_id, level_number, score, total_questions, accuracy_percent, time_spent_seconds, completed_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
                    ON CONFLICT (id) DO NOTHING;
                    """, (attempt_id, user_id, subject_id, level_number, score, total_questions, accuracy_percent, time_spent_seconds))
                    
                    pg_ans = [
                        (attempt_id, user_id, a[2], a[3], a[4], a[5])
                        for a in answers_to_insert
                    ]
                    from psycopg2.extras import execute_values
                    execute_values(pg_cur, """
                    INSERT INTO public.quiz_answers (attempt_id, user_id, question_id, selected_option, correct_option, is_correct)
                    VALUES %s;
                    """, pg_ans)
                    pg_conn.commit()
                    pg_cur.close()
        except Exception:
            pass

        # Update student telemetry in SQLite
        update_user_telemetry(
            user_id=user_id,
            solved_increment=total_questions,
            mastery_delta=round((score / max(total_questions, 1)) * 0.5, 2)
        )

    except Exception as e:
        conn.rollback()
        conn.close()
        raise e
    finally:
        try:
            conn.close()
        except Exception:
            pass

    next_level = min(level_number + 1, 5)
    is_unlocked_next = level_number < 5

    return {
        "attempt_id": attempt_id,
        "subject_id": subject_id,
        "level_number": level_number,
        "score": score,
        "total_questions": total_questions,
        "accuracy_percent": accuracy_percent,
        "time_spent_seconds": time_spent_seconds,
        "is_unlocked_next": is_unlocked_next,
        "next_level_number": next_level,
        "answers_review": answers_review,
        "completed_at": now
    }


def get_quiz_attempt_review(user_id: str, attempt_id: str) -> Optional[dict]:
    """
    Reconstructs the persistent 10-question answer key from quiz_attempts and quiz_answers
    with strict user isolation, supporting both Supabase Cloud PostgreSQL and SQLite.
    """
    # 1. Supabase Cloud PostgreSQL check
    try:
        from backend.services.supabase_service import get_pg_connection, is_supabase_configured
        from psycopg2.extras import RealDictCursor
        if is_supabase_configured():
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor(cursor_factory=RealDictCursor) as pg_cur:
                    pg_cur.execute("""
                    SELECT qa.*, ps.title as subject_title
                    FROM public.quiz_attempts qa
                    JOIN public.practice_subjects ps ON qa.subject_id = ps.id
                    WHERE qa.id = %s AND qa.user_id = %s
                    """, (attempt_id, user_id))
                    attempt_row = pg_cur.fetchone()
                    if attempt_row:
                        attempt = dict(attempt_row)
                        if hasattr(attempt.get("completed_at"), "isoformat"):
                            attempt["completed_at"] = attempt["completed_at"].isoformat()
                        pg_cur.execute("""
                        SELECT 
                            ans.question_id, ans.selected_option, ans.correct_option, ans.is_correct,
                            pq.question_text, pq.option_a, pq.option_b, pq.option_c, pq.option_d,
                            pq.explanation, pq.topic, pq.order_index
                        FROM public.quiz_answers ans
                        JOIN public.practice_questions pq ON ans.question_id = pq.id
                        WHERE ans.attempt_id = %s AND ans.user_id = %s
                        ORDER BY pq.order_index ASC
                        """, (attempt_id, user_id))
                        rows = pg_cur.fetchall()
                        answers_review = []
                        for r in rows:
                            options = [r["option_a"], r["option_b"], r["option_c"], r["option_d"]]
                            answers_review.append({
                                "question_id": r["question_id"],
                                "order_index": r["order_index"],
                                "question_text": r["question_text"],
                                "options": options,
                                "selected_option": r["selected_option"],
                                "correct_option": r["correct_option"],
                                "is_correct": bool(r["is_correct"]),
                                "explanation": r["explanation"],
                                "topic": r["topic"]
                            })
                        attempt["answers_review"] = answers_review
                        return attempt
    except Exception as err:
        logger.warning(f"[get_quiz_attempt_review] Supabase fetch fallback: {err}")

    # 2. SQLite local fallback
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT qa.*, ps.title as subject_title
    FROM quiz_attempts qa
    JOIN practice_subjects ps ON qa.subject_id = ps.id
    WHERE qa.id = ? AND qa.user_id = ?
    """, (attempt_id, user_id))
    attempt_row = cursor.fetchone()
    if not attempt_row:
        conn.close()
        return None

    attempt = dict(attempt_row)

    cursor.execute("""
    SELECT 
        ans.question_id, ans.selected_option, ans.correct_option, ans.is_correct,
        pq.question_text, pq.option_a, pq.option_b, pq.option_c, pq.option_d,
        pq.explanation, pq.topic, pq.order_index
    FROM quiz_answers ans
    JOIN practice_questions pq ON ans.question_id = pq.id
    WHERE ans.attempt_id = ? AND ans.user_id = ?
    ORDER BY pq.order_index ASC
    """, (attempt_id, user_id))

    rows = cursor.fetchall()
    conn.close()

    answers_review = []
    for r in rows:
        options = [r["option_a"], r["option_b"], r["option_c"], r["option_d"]]
        answers_review.append({
            "question_id": r["question_id"],
            "order_index": r["order_index"],
            "question_text": r["question_text"],
            "options": options,
            "selected_option": r["selected_option"],
            "correct_option": r["correct_option"],
            "is_correct": bool(r["is_correct"]),
            "explanation": r["explanation"],
            "topic": r["topic"]
        })

    attempt["answers_review"] = answers_review
    return attempt


def get_user_quiz_history(user_id: str, limit: int = 50) -> list[dict]:
    """Retrieves chronological quiz attempts history for the authenticated user from Supabase or SQLite."""
    # 1. Supabase Cloud PostgreSQL check
    try:
        from backend.services.supabase_service import get_pg_connection, is_supabase_configured
        from psycopg2.extras import RealDictCursor
        if is_supabase_configured():
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor(cursor_factory=RealDictCursor) as pg_cur:
                    pg_cur.execute("""
                    SELECT qa.id, qa.subject_id, ps.title as subject_title, qa.level_number,
                           qa.score, qa.total_questions, qa.accuracy_percent, qa.time_spent_seconds, qa.completed_at
                    FROM public.quiz_attempts qa
                    JOIN public.practice_subjects ps ON qa.subject_id = ps.id
                    WHERE qa.user_id = %s
                    ORDER BY qa.completed_at DESC
                    LIMIT %s
                    """, (user_id, limit))
                    rows = [dict(r) for r in pg_cur.fetchall()]
                    if rows:
                        for r in rows:
                            if hasattr(r.get("completed_at"), "isoformat"):
                                r["completed_at"] = r["completed_at"].isoformat()
                        return rows
    except Exception as err:
        logger.warning(f"[get_user_quiz_history] Supabase fetch fallback: {err}")

    # 2. SQLite local fallback
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT qa.id, qa.subject_id, ps.title as subject_title, qa.level_number,
           qa.score, qa.total_questions, qa.accuracy_percent, qa.time_spent_seconds, qa.completed_at
    FROM quiz_attempts qa
    JOIN practice_subjects ps ON qa.subject_id = ps.id
    WHERE qa.user_id = ?
    ORDER BY qa.completed_at DESC
    LIMIT ?
    """, (user_id, limit))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_user_progress_summary(user_id: str) -> dict:
    """Single Source of Truth for Progress Engine across Practice, Dashboard, and Progress pages."""
    # Attempt querying Supabase PostgreSQL first for production persistence
    try:
        from backend.services.supabase_service import get_pg_connection, is_supabase_configured
        from psycopg2.extras import RealDictCursor
        if is_supabase_configured():
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor(cursor_factory=RealDictCursor) as pg_cur:
                    pg_cur.execute("SELECT id, title, description, icon, order_index FROM public.practice_subjects ORDER BY order_index ASC")
                    subjects_raw = [dict(r) for r in pg_cur.fetchall()]
                    if subjects_raw:
                        subjects_progress = []
                        total_completed_levels = 0
                        for s in subjects_raw:
                            s_id = s["id"]
                            pg_cur.execute("""
                            SELECT DISTINCT level_number, MAX(score) as best_score, MAX(accuracy_percent) as best_acc
                            FROM public.quiz_attempts
                            WHERE user_id = %s AND subject_id = %s
                            GROUP BY level_number
                            """, (user_id, s_id))
                            completed_rows = [dict(r) for r in pg_cur.fetchall()]
                            completed_cnt = len(completed_rows)
                            total_completed_levels += completed_cnt
                            avg_acc = round(sum(r["best_acc"] for r in completed_rows) / len(completed_rows), 1) if completed_rows else 0.0

                            subjects_progress.append({
                                "id": s_id,
                                "title": s["title"],
                                "icon": s["icon"],
                                "description": s["description"],
                                "completed_levels": completed_cnt,
                                "total_levels": 5,
                                "progress_percent": round((completed_cnt / 5.0) * 100, 1),
                                "accuracy_percent": avg_acc,
                                "unlocked_level": min(completed_cnt + 1, 5)
                            })

                        pg_cur.execute("SELECT COUNT(*), SUM(is_correct) FROM public.quiz_answers WHERE user_id = %s", (user_id,))
                        ans_stats = pg_cur.fetchone()
                        total_answers = (ans_stats["count"] if ans_stats and "count" in ans_stats else 0)
                        correct_answers = (ans_stats["sum"] if ans_stats and "sum" in ans_stats and ans_stats["sum"] is not None else 0)
                        overall_accuracy = round((correct_answers / max(total_answers, 1)) * 100, 1) if total_answers > 0 else 0.0

                        pg_cur.execute("""
                        SELECT qa.id, qa.subject_id, ps.title as subject_title, qa.level_number, qa.score, qa.total_questions, qa.accuracy_percent, qa.completed_at
                        FROM public.quiz_attempts qa
                        JOIN public.practice_subjects ps ON qa.subject_id = ps.id
                        WHERE qa.user_id = %s
                        ORDER BY qa.completed_at DESC
                        LIMIT 10
                        """, (user_id,))
                        recent_activity = []
                        for r in pg_cur.fetchall():
                            rec = dict(r)
                            if hasattr(rec.get("completed_at"), "isoformat"):
                                rec["completed_at"] = rec["completed_at"].isoformat()
                            recent_activity.append(rec)

                        total_levels_count = len(subjects_raw) * 5
                        overall_progress_percent = round((total_completed_levels / float(total_levels_count or 25)) * 100, 1)

                        return {
                            "completed_levels_count": total_completed_levels,
                            "total_levels_count": total_levels_count,
                            "overall_progress_percent": overall_progress_percent,
                            "total_questions_solved": total_answers,
                            "total_correct_answers": correct_answers,
                            "overall_accuracy_percent": overall_accuracy,
                            "subjects": subjects_progress,
                            "recent_activity": recent_activity
                        }
    except Exception:
        pass

    # Seamless fallback to SQLite
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM practice_subjects ORDER BY order_index ASC")
    subjects_raw = [dict(r) for r in cursor.fetchall()]

    subjects_progress = []
    total_completed_levels = 0

    for s in subjects_raw:
        s_id = s["id"]
        cursor.execute("""
        SELECT DISTINCT level_number, MAX(score) as best_score, MAX(accuracy_percent) as best_acc
        FROM quiz_attempts
        WHERE user_id = ? AND subject_id = ?
        GROUP BY level_number
        """, (user_id, s_id))
        completed_rows = cursor.fetchall()
        completed_cnt = len(completed_rows)
        total_completed_levels += completed_cnt
        avg_acc = round(sum(r["best_acc"] for r in completed_rows) / len(completed_rows), 1) if completed_rows else 0.0

        subjects_progress.append({
            "id": s_id,
            "title": s["title"],
            "icon": s["icon"],
            "description": s["description"],
            "completed_levels": completed_cnt,
            "total_levels": 5,
            "progress_percent": round((completed_cnt / 5.0) * 100, 1),
            "accuracy_percent": avg_acc,
            "unlocked_level": min(completed_cnt + 1, 5)
        })

    # Overall Metrics from all quiz answers for this user
    cursor.execute("SELECT COUNT(*), SUM(is_correct) FROM quiz_answers WHERE user_id = ?", (user_id,))
    ans_stats = cursor.fetchone()
    total_answers = ans_stats[0] or 0
    correct_answers = ans_stats[1] or 0
    overall_accuracy = round((correct_answers / max(total_answers, 1)) * 100, 1) if total_answers > 0 else 0.0

    # Recent activity
    cursor.execute("""
    SELECT qa.id, qa.subject_id, ps.title as subject_title, qa.level_number, qa.score, qa.total_questions, qa.accuracy_percent, qa.completed_at
    FROM quiz_attempts qa
    JOIN practice_subjects ps ON qa.subject_id = ps.id
    WHERE qa.user_id = ?
    ORDER BY qa.completed_at DESC
    LIMIT 10
    """, (user_id,))
    recent_activity = [dict(r) for r in cursor.fetchall()]

    conn.close()

    total_levels_count = len(subjects_raw) * 5
    overall_progress_percent = round((total_completed_levels / float(total_levels_count or 25)) * 100, 1)

    return {
        "completed_levels_count": total_completed_levels,
        "total_levels_count": total_levels_count,
        "overall_progress_percent": overall_progress_percent,
        "total_questions_solved": total_answers,
        "total_correct_answers": correct_answers,
        "overall_accuracy_percent": overall_accuracy,
        "subjects": subjects_progress,
        "recent_activity": recent_activity
    }


def get_student_test_history_and_activity(student_id: str) -> dict:
    """Returns comprehensive test history, quiz attempts, and activity timeline for educator inspection."""
    user = get_user_by_id(student_id)
    student_name = user.get("full_name", "Student") if user else "Student"
    student_email = user.get("email", "") if user else ""

    quiz_attempts = []
    total_answers = 0
    correct_answers = 0

    # Try Supabase PostgreSQL first
    try:
        from backend.services.supabase_service import get_pg_connection, is_supabase_configured
        from psycopg2.extras import RealDictCursor
        if is_supabase_configured():
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor(cursor_factory=RealDictCursor) as pg_cur:
                    pg_cur.execute("""
                    SELECT qa.id, qa.subject_id, COALESCE(ps.title, qa.subject_id) as subject_title,
                           qa.level_number, qa.score, qa.total_questions, qa.accuracy_percent,
                           qa.time_spent_seconds, qa.completed_at
                    FROM public.quiz_attempts qa
                    LEFT JOIN public.practice_subjects ps ON qa.subject_id = ps.id
                    WHERE qa.user_id = %s
                    ORDER BY qa.completed_at DESC
                    LIMIT 50
                    """, (student_id,))
                    for r in pg_cur.fetchall():
                        rec = dict(r)
                        if hasattr(rec.get("completed_at"), "isoformat"):
                            rec["completed_at"] = rec["completed_at"].isoformat()
                        rec["status"] = "Passed" if (rec.get("accuracy_percent") or 0) >= 60 else "Needs Review"
                        quiz_attempts.append(rec)

                    pg_cur.execute("SELECT COUNT(*), SUM(is_correct) FROM public.quiz_answers WHERE user_id = %s", (student_id,))
                    ans_stats = pg_cur.fetchone()
                    if ans_stats:
                        total_answers = ans_stats["count"] if "count" in ans_stats else 0
                        correct_answers = ans_stats["sum"] if "sum" in ans_stats and ans_stats["sum"] is not None else 0
    except Exception:
        pass

    # Fallback to SQLite if no quiz attempts found from PostgreSQL
    if not quiz_attempts:
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT qa.id, qa.subject_id, COALESCE(ps.title, qa.subject_id) as subject_title,
                   qa.level_number, qa.score, qa.total_questions, qa.accuracy_percent,
                   qa.time_spent_seconds, qa.completed_at
            FROM quiz_attempts qa
            LEFT JOIN practice_subjects ps ON qa.subject_id = ps.id
            WHERE qa.user_id = ?
            ORDER BY qa.completed_at DESC
            LIMIT 50
            """, (student_id,))
            for r in cursor.fetchall():
                rec = dict(r)
                rec["status"] = "Passed" if (rec.get("accuracy_percent") or 0) >= 60 else "Needs Review"
                quiz_attempts.append(rec)

            cursor.execute("SELECT COUNT(*), SUM(is_correct) FROM quiz_answers WHERE user_id = ?", (student_id,))
            ans_stats = cursor.fetchone()
            if ans_stats:
                total_answers = ans_stats[0] or 0
                correct_answers = ans_stats[1] or 0
        except Exception:
            pass
        finally:
            conn.close()

    # Compute summary
    total_tests = len(quiz_attempts)
    avg_accuracy = round(sum(q["accuracy_percent"] for q in quiz_attempts) / max(total_tests, 1), 1) if total_tests > 0 else 0.0
    completed_levels = len({f"{q['subject_id']}_{q['level_number']}" for q in quiz_attempts})

    # Build chronological activity events
    activity_timeline = []
    for q in quiz_attempts:
        mins = round((q.get("time_spent_seconds") or 0) / 60, 1)
        activity_timeline.append({
            "type": "quiz_completed",
            "title": f"Completed {q.get('subject_title', 'Subject')} Level {q.get('level_number', 1)} Quiz",
            "description": f"Scored {q.get('score', 0)}/{q.get('total_questions', 10)} ({q.get('accuracy_percent', 0)}% accuracy) in {mins} min",
            "status": q.get("status", "Completed"),
            "timestamp": q.get("completed_at", "")
        })

    return {
        "status": "success",
        "student_id": student_id,
        "student_name": student_name,
        "student_email": student_email,
        "summary": {
            "total_tests_completed": total_tests,
            "total_questions_solved": total_answers,
            "total_correct_answers": correct_answers,
            "overall_accuracy_percent": avg_accuracy,
            "completed_levels_count": completed_levels
        },
        "quiz_history": quiz_attempts,
        "activity_timeline": activity_timeline
    }


# =========================================================================
# AI PERSONALIZED LEARNING ROADMAP DATA ACCESS
# =========================================================================

def get_active_roadmap(user_id: str) -> Optional[dict]:
    """Fetches active AI Learning Roadmap for authenticated user from Cloud PostgreSQL or SQLite."""
    # 1. Check Cloud PostgreSQL
    try:
        from backend.services.supabase_service import get_pg_connection, is_supabase_configured
        from psycopg2.extras import RealDictCursor
        if is_supabase_configured():
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor(cursor_factory=RealDictCursor) as pg_cur:
                    pg_cur.execute("""
                    SELECT id, user_id, title, summary, goal, estimated_duration, progress_snapshot_hash, roadmap_json, status, created_at, updated_at
                    FROM public.ai_learning_roadmaps
                    WHERE user_id = %s AND status = 'active'
                    ORDER BY updated_at DESC
                    LIMIT 1
                    """, (user_id,))
                    row = pg_cur.fetchone()
                    if row:
                        d = dict(row)
                        rm = d.get("roadmap_json")
                        roadmap_data = json.loads(rm) if isinstance(rm, str) else (rm or {})
                        return {
                            "id": d["id"],
                            "user_id": d["user_id"],
                            "title": d["title"],
                            "summary": d["summary"],
                            "goal": d["goal"],
                            "estimated_duration": d["estimated_duration"],
                            "progress_snapshot_hash": d["progress_snapshot_hash"],
                            "nodes": roadmap_data.get("nodes", []),
                            "status": d["status"],
                            "created_at": str(d["created_at"]),
                            "updated_at": str(d["updated_at"])
                        }
    except Exception as err:
        logger.warning(f"[Supabase] get_active_roadmap warning: {err}")

    # 2. SQLite fallback
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, user_id, title, summary, goal, estimated_duration, progress_snapshot_hash, roadmap_json, status, created_at, updated_at
        FROM ai_learning_roadmaps
        WHERE user_id = ? AND status = 'active'
        ORDER BY updated_at DESC
        LIMIT 1
        """, (user_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        try:
            roadmap_data = json.loads(row["roadmap_json"])
        except Exception:
            roadmap_data = {}

        return {
            "id": row["id"],
            "user_id": row["user_id"],
            "title": row["title"],
            "summary": row["summary"],
            "goal": row["goal"],
            "estimated_duration": row["estimated_duration"],
            "progress_snapshot_hash": row["progress_snapshot_hash"],
            "nodes": roadmap_data.get("nodes", []),
            "status": row["status"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"]
        }
    except Exception:
        return None


def save_learning_roadmap(
    user_id: str,
    title: str,
    summary: str,
    goal: str,
    estimated_duration: str,
    progress_snapshot_hash: str,
    roadmap_data: dict
) -> dict:
    """Stores a validated AI Learning Roadmap in Cloud PostgreSQL or SQLite, archiving previous ones."""
    import uuid
    roadmap_id = f"rdm_{uuid.uuid4().hex[:12]}"
    now = datetime.utcnow().isoformat()

    # 1. Cloud PostgreSQL
    try:
        from backend.services.supabase_service import get_pg_connection, is_supabase_configured
        if is_supabase_configured():
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor() as pg_cur:
                    pg_cur.execute("UPDATE public.ai_learning_roadmaps SET status = 'archived' WHERE user_id = %s AND status = 'active'", (user_id,))
                    pg_cur.execute("""
                    INSERT INTO public.ai_learning_roadmaps (
                        id, user_id, title, summary, goal, estimated_duration,
                        progress_snapshot_hash, roadmap_json, status, created_at, updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'active', NOW(), NOW())
                    """, (
                        roadmap_id, user_id, title, summary, goal, estimated_duration,
                        progress_snapshot_hash, json.dumps(roadmap_data)
                    ))
                    pg_conn.commit()
    except Exception as err:
        logger.warning(f"[Supabase] save_learning_roadmap warning: {err}")

    # 2. SQLite fallback
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE ai_learning_roadmaps SET status = 'archived' WHERE user_id = ? AND status = 'active'", (user_id,))
        cursor.execute("""
        INSERT INTO ai_learning_roadmaps (
            id, user_id, title, summary, goal, estimated_duration,
            progress_snapshot_hash, roadmap_json, status, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'active', ?, ?)
        """, (
            roadmap_id, user_id, title, summary, goal, estimated_duration,
            progress_snapshot_hash, json.dumps(roadmap_data), now, now
        ))
        conn.commit()
        conn.close()
    except Exception:
        pass

    return {
        "id": roadmap_id,
        "user_id": user_id,
        "title": title,
        "summary": summary,
        "goal": goal,
        "estimated_duration": estimated_duration,
        "progress_snapshot_hash": progress_snapshot_hash,
        "nodes": roadmap_data.get("nodes", []),
        "status": "active",
        "created_at": now,
        "updated_at": now
    }


# =========================================================================
# NOTES AI CONVERSATIONS & MESSAGES (PERSISTENT MULTI-TURN RAG)
# =========================================================================

def get_or_create_ai_conversation(user_id: str, chapter_id: Optional[str] = None) -> str:
    """Retrieves or creates conversation ID for user and chapter."""
    import uuid
    conn = get_db_connection()
    cursor = conn.cursor()

    if chapter_id:
        cursor.execute("SELECT id FROM ai_conversations WHERE user_id = ? AND chapter_id = ? ORDER BY updated_at DESC LIMIT 1", (user_id, chapter_id))
    else:
        cursor.execute("SELECT id FROM ai_conversations WHERE user_id = ? AND chapter_id IS NULL ORDER BY updated_at DESC LIMIT 1", (user_id,))

    row = cursor.fetchone()
    if row:
        conv_id = row["id"]
        conn.close()
        return conv_id

    conv_id = f"cnv_{uuid.uuid4().hex[:12]}"
    now = datetime.utcnow().isoformat()
    cursor.execute("""
    INSERT INTO ai_conversations (id, user_id, chapter_id, title, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (conv_id, user_id, chapter_id, f"Study Session on {chapter_id or 'General'}", now, now))
    conn.commit()
    conn.close()
    return conv_id


def get_conversation_history(conversation_id: str, limit: int = 10) -> List[dict]:
    """Retrieves previous messages for contextual follow-up."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT role, content, source_json, created_at
    FROM ai_messages
    WHERE conversation_id = ?
    ORDER BY created_at ASC
    LIMIT ?
    """, (conversation_id, limit))
    rows = cursor.fetchall()
    conn.close()

    history = []
    for r in rows:
        source_obj = json.loads(r["source_json"]) if r["source_json"] else None
        history.append({
            "role": r["role"],
            "content": r["content"],
            "source": source_obj,
            "created_at": r["created_at"]
        })
    return history


def record_ai_message(conversation_id: str, role: str, content: str, source_obj: Optional[dict] = None) -> None:
    """Records a user or AI message into SQLite."""
    import uuid
    msg_id = f"msg_{uuid.uuid4().hex[:12]}"
    now = datetime.utcnow().isoformat()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO ai_messages (id, conversation_id, role, content, source_json, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (msg_id, conversation_id, role, content, json.dumps(source_obj) if source_obj else None, now))

    cursor.execute("UPDATE ai_conversations SET updated_at = ? WHERE id = ?", (now, conversation_id))
    conn.commit()
    conn.close()


# =========================================================================
# SCHEMA MIGRATION HELPER (SAFE ADD COLUMNS)
# =========================================================================

def _safe_add_columns(conn):
    """Adds new columns to existing tables without error if already present."""
    migrations = [
        ("ai_conversations", "mode", "TEXT DEFAULT 'socratic'"),
        ("ai_conversations", "subject", "TEXT DEFAULT ''"),
        ("ai_conversations", "persona", "TEXT DEFAULT 'balanced'"),
        ("ai_conversations", "summary", "TEXT DEFAULT ''"),
        ("ai_conversations", "conversation_type", "TEXT DEFAULT 'notes'"),
        ("ai_messages", "mode", "TEXT DEFAULT ''"),
    ]
    cursor = conn.cursor()
    for table, col, col_type in migrations:
        try:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col} {col_type}")
        except Exception:
            pass  # Column already exists
    conn.commit()


# =========================================================================
# AI MENTOR CONVERSATIONS — FULL CRUD
# =========================================================================

def create_mentor_conversation(user_id: str, title: str, mode: str = "socratic",
                               subject: str = "", persona: str = "balanced") -> str:
    """Creates a new AI Mentor conversation and returns its ID."""
    conv_id = f"mcnv_{uuid.uuid4().hex[:12]}"
    now = datetime.utcnow().isoformat()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO ai_conversations (id, user_id, chapter_id, title, mode, subject, persona, summary, conversation_type, created_at, updated_at)
    VALUES (?, ?, NULL, ?, ?, ?, ?, '', 'mentor', ?, ?)
    """, (conv_id, user_id, title, mode, subject, persona, now, now))
    conn.commit()
    conn.close()
    return conv_id


def get_mentor_conversations(user_id: str, limit: int = 30, search_query: str = "") -> List[dict]:
    """Lists AI Mentor conversations for a user, optionally filtered by search."""
    conn = get_db_connection()
    cursor = conn.cursor()
    if search_query:
        q = f"%{search_query}%"
        cursor.execute("""
        SELECT c.id, c.title, c.mode, c.subject, c.persona, c.summary, c.created_at, c.updated_at,
               (SELECT COUNT(*) FROM ai_messages WHERE conversation_id = c.id) as msg_count
        FROM ai_conversations c
        WHERE c.user_id = ? AND c.conversation_type = 'mentor' AND (c.title LIKE ? OR c.subject LIKE ?)
        ORDER BY c.updated_at DESC LIMIT ?
        """, (user_id, q, q, limit))
    else:
        cursor.execute("""
        SELECT c.id, c.title, c.mode, c.subject, c.persona, c.summary, c.created_at, c.updated_at,
               (SELECT COUNT(*) FROM ai_messages WHERE conversation_id = c.id) as msg_count
        FROM ai_conversations c
        WHERE c.user_id = ? AND c.conversation_type = 'mentor'
        ORDER BY c.updated_at DESC LIMIT ?
        """, (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_mentor_conversation(conv_id: str, user_id: str) -> Optional[dict]:
    """Gets a single conversation with ownership check."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, title, mode, subject, persona, summary, conversation_type, created_at, updated_at
    FROM ai_conversations WHERE id = ? AND user_id = ?
    """, (conv_id, user_id))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_mentor_messages(conv_id: str, limit: int = 50) -> List[dict]:
    """Retrieves messages for a mentor conversation."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, role, content, mode, source_json, created_at
    FROM ai_messages WHERE conversation_id = ? ORDER BY created_at ASC LIMIT ?
    """, (conv_id, limit))
    rows = cursor.fetchall()
    conn.close()
    results = []
    for r in rows:
        msg = dict(r)
        if msg.get("source_json"):
            try:
                msg["source"] = json.loads(msg["source_json"])
            except Exception:
                msg["source"] = None
        del msg["source_json"]
        results.append(msg)
    return results


def save_mentor_message(conv_id: str, role: str, content: str, mode: str = "",
                        metadata: Optional[dict] = None) -> str:
    """Saves a mentor message and updates conversation timestamp."""
    msg_id = f"mmsg_{uuid.uuid4().hex[:12]}"
    now = datetime.utcnow().isoformat()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO ai_messages (id, conversation_id, role, content, mode, source_json, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (msg_id, conv_id, role, content, mode, json.dumps(metadata) if metadata else None, now))
    cursor.execute("UPDATE ai_conversations SET updated_at = ? WHERE id = ?", (now, conv_id))
    conn.commit()
    conn.close()
    return msg_id


def update_conversation_meta(conv_id: str, **kwargs) -> None:
    """Updates conversation metadata (title, mode, subject, summary, persona)."""
    allowed = {"title", "mode", "subject", "summary", "persona"}
    updates = {k: v for k, v in kwargs.items() if k in allowed and v is not None}
    if not updates:
        return
    now = datetime.utcnow().isoformat()
    updates["updated_at"] = now
    set_clause = ", ".join([f"{k} = ?" for k in updates])
    vals = list(updates.values()) + [conv_id]
    conn = get_db_connection()
    conn.execute(f"UPDATE ai_conversations SET {set_clause} WHERE id = ?", vals)
    conn.commit()
    conn.close()


def delete_mentor_conversation(conv_id: str, user_id: str) -> bool:
    """Deletes a conversation with ownership check. Returns True if deleted."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ai_conversations WHERE id = ? AND user_id = ?", (conv_id, user_id))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


# =========================================================================
# USER AI PREFERENCES
# =========================================================================

def get_ai_preferences(user_id: str) -> dict:
    """Gets or creates AI preferences for a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_ai_preferences WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row:
        conn.close()
        return dict(row)
    now = datetime.utcnow().isoformat()
    cursor.execute("""
    INSERT INTO user_ai_preferences (user_id, persona, daily_study_minutes, preferred_language, updated_at)
    VALUES (?, 'balanced', 45, 'en', ?)
    """, (user_id, now))
    conn.commit()
    conn.close()
    return {"user_id": user_id, "persona": "balanced", "daily_study_minutes": 45, "preferred_language": "en"}


def update_ai_preferences(user_id: str, persona: str = None, daily_study_minutes: int = None,
                          preferred_language: str = None) -> dict:
    """Updates user AI preferences. Creates if not exists."""
    get_ai_preferences(user_id)  # Ensure row exists
    now = datetime.utcnow().isoformat()
    updates = {"updated_at": now}
    if persona is not None:
        updates["persona"] = persona
    if daily_study_minutes is not None:
        updates["daily_study_minutes"] = daily_study_minutes
    if preferred_language is not None:
        updates["preferred_language"] = preferred_language
    set_clause = ", ".join([f"{k} = ?" for k in updates])
    vals = list(updates.values()) + [user_id]
    conn = get_db_connection()
    conn.execute(f"UPDATE user_ai_preferences SET {set_clause} WHERE user_id = ?", vals)
    conn.commit()
    conn.close()
    return get_ai_preferences(user_id)


# =========================================================================
# SMART REVISION SESSIONS & TELEMETRY PERSISTENCE
# =========================================================================

def save_revision_session(
    user_id: str,
    topic: str,
    subject_id: str,
    duration_minutes: float = 15.0,
    steps_total: int = 4,
    steps_completed: int = 4,
    score: int = 0,
    total_questions: int = 0,
    review_mode: str = "standard",
    resources_used: Optional[List[str]] = None,
    priority_score: float = 0.0
) -> Dict[str, Any]:
    """
    Persists a completed or partially completed smart revision session to SQLite.
    Updates questions_solved in user_telemetry if questions were completed.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    session_id = f"rev_{uuid.uuid4().hex[:12]}"
    now = datetime.utcnow().isoformat()
    res_json = json.dumps(resources_used or [])

    cursor.execute("""
    INSERT INTO revision_sessions (
        id, user_id, topic, subject_id, priority_score, status,
        duration_minutes, steps_total, steps_completed, score,
        total_questions, review_mode, resources_used_json, created_at, completed_at
    ) VALUES (?, ?, ?, ?, ?, 'completed', ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        session_id, user_id, topic, subject_id, priority_score,
        duration_minutes, steps_total, steps_completed, score,
        total_questions, review_mode, res_json, now, now
    ))

    # Update questions solved in user_telemetry if score / questions answered
    if total_questions > 0:
        cursor.execute("""
        UPDATE user_telemetry 
        SET questions_solved = questions_solved + ?, updated_at = ?
        WHERE user_id = ?
        """, (total_questions, now, user_id))

    conn.commit()
    conn.close()

    return {
        "id": session_id,
        "user_id": user_id,
        "topic": topic,
        "subject_id": subject_id,
        "duration_minutes": duration_minutes,
        "score": score,
        "total_questions": total_questions,
        "review_mode": review_mode,
        "completed_at": now
    }


def get_user_revision_history(user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Retrieves authenticated student's genuine revision history from SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        id, topic, subject_id, duration_minutes, steps_total,
        steps_completed, score, total_questions, review_mode,
        resources_used_json, completed_at
    FROM revision_sessions
    WHERE user_id = ?
    ORDER BY completed_at DESC
    LIMIT ?
    """, (user_id, limit))

    rows = cursor.fetchall()
    conn.close()

    subject_names = {
        "phys": "Physics",
        "chem": "Chemistry",
        "math": "Mathematics",
        "cs": "Computer Science",
        "bio": "Biology"
    }

    history = []
    for r in rows:
        history.append({
            "id": r["id"],
            "topic": r["topic"],
            "subject_id": r["subject_id"],
            "subject_title": subject_names.get(r["subject_id"], r["subject_id"].upper()),
            "duration_minutes": round(r["duration_minutes"], 1),
            "steps_total": r["steps_total"],
            "steps_completed": r["steps_completed"],
            "score": r["score"],
            "total_questions": r["total_questions"],
            "review_mode": r["review_mode"],
            "resources_used": json.loads(r["resources_used_json"] or "[]"),
            "completed_at": r["completed_at"]
        })
    return history


def get_user_revision_stats(user_id: str) -> Dict[str, Any]:
    """Calculates aggregate revision statistics from real records."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        COUNT(*) as total_revisions,
        COALESCE(SUM(duration_minutes), 0) as total_minutes_revised,
        COUNT(DISTINCT topic) as distinct_topics_revised,
        MAX(completed_at) as last_revision_at
    FROM revision_sessions
    WHERE user_id = ?
    """, (user_id,))
    row = cursor.fetchone()
    conn.close()

    return {
        "total_revisions": row["total_revisions"] if row else 0,
        "total_minutes_revised": round(row["total_minutes_revised"], 1) if row else 0,
        "distinct_topics_revised": row["distinct_topics_revised"] if row else 0,
        "last_revision_at": row["last_revision_at"] if row else None
    }


def record_assessment_attempt(
    attempt_id: str,
    user_id: str,
    assessment_id: str,
    title: str,
    score: int,
    max_score: int,
    accuracy_percent: float,
    percentile: float,
    time_spent_seconds: int,
    subject_breakdown: List[Dict[str, Any]],
    solutions: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Persists a diagnostic assessment attempt to SQLite.
    Also syncs answered questions into `quiz_attempts` and `quiz_answers`
    so the Learning Genome, telemetry, and smart revision queue reflect the performance.
    """
    now = datetime.utcnow().isoformat()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO assessment_attempts (
            id, user_id, assessment_id, title, score, max_score, accuracy_percent, percentile,
            time_spent_seconds, subject_breakdown_json, solutions_json, completed_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            attempt_id, user_id, assessment_id, title, score, max_score, accuracy_percent, percentile,
            time_spent_seconds, json.dumps(subject_breakdown), json.dumps(solutions), now
        ))

        # Log into quiz_attempts and quiz_answers for Learning Genome integration
        from collections import defaultdict
        subj_solutions = defaultdict(list)
        for s in solutions:
            subj_id = s.get("subject_id", "physics").lower()
            subj_solutions[subj_id].append(s)

        for subj_id, s_list in subj_solutions.items():
            sub_total = len(s_list)
            sub_correct = sum(1 for item in s_list if item.get("is_correct"))
            sub_acc = round((sub_correct / max(sub_total, 1)) * 100.0, 1)
            sub_attempt_id = f"{attempt_id}_{subj_id[:4]}"

            cursor.execute("""
            INSERT OR REPLACE INTO quiz_attempts (
                id, user_id, subject_id, level_number, score, total_questions, accuracy_percent, time_spent_seconds, completed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                sub_attempt_id, user_id, subj_id, 0, sub_correct, sub_total, sub_acc,
                int(time_spent_seconds / max(len(subj_solutions), 1)), now
            ))

            for item in s_list:
                cursor.execute("""
                INSERT INTO quiz_answers (
                    attempt_id, user_id, question_id, selected_option, correct_option, is_correct
                ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    sub_attempt_id, user_id, item.get("question_id", "q_gen"),
                    item.get("selected_option", -1), item.get("correct_option", 0),
                    1 if item.get("is_correct") else 0
                ))

        conn.commit()

        # Update telemetry
        update_user_telemetry(
            user_id=user_id,
            solved_increment=len(solutions),
            mastery_delta=round((accuracy_percent / 100.0) * 1.5, 2)
        )
    except Exception as e:
        conn.rollback()
        conn.close()
        raise e
    finally:
        try:
            conn.close()
        except Exception:
            pass

    return {
        "id": attempt_id,
        "user_id": user_id,
        "assessment_id": assessment_id,
        "title": title,
        "score": score,
        "max_score": max_score,
        "accuracy_percent": accuracy_percent,
        "percentile": percentile,
        "time_spent_seconds": time_spent_seconds,
        "subject_breakdown": subject_breakdown,
        "solutions": solutions,
        "completed_at": now
    }


def get_user_assessment_history(user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Retrieves all past assessment attempts for a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, user_id, assessment_id, title, score, max_score, accuracy_percent, percentile,
           time_spent_seconds, subject_breakdown_json, completed_at
    FROM assessment_attempts
    WHERE user_id = ?
    ORDER BY completed_at DESC
    LIMIT ?
    """, (user_id, limit))
    rows = cursor.fetchall()
    conn.close()

    history = []
    for r in rows:
        history.append({
            "id": r["id"],
            "assessment_id": r["assessment_id"],
            "title": r["title"],
            "score": r["score"],
            "max_score": r["max_score"],
            "accuracy_percent": r["accuracy_percent"],
            "percentile": r["percentile"],
            "time_spent_seconds": r["time_spent_seconds"],
            "subject_breakdown": json.loads(r["subject_breakdown_json"]) if r["subject_breakdown_json"] else [],
            "completed_at": r["completed_at"]
        })
    return history


def get_assessment_attempt_by_id(attempt_id: str, user_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves full details of a specific assessment attempt including solutions."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, user_id, assessment_id, title, score, max_score, accuracy_percent, percentile,
           time_spent_seconds, subject_breakdown_json, solutions_json, completed_at
    FROM assessment_attempts
    WHERE id = ? AND user_id = ?
    """, (attempt_id, user_id))
    r = cursor.fetchone()
    conn.close()
    if not r:
        return None

    return {
        "id": r["id"],
        "assessment_id": r["assessment_id"],
        "title": r["title"],
        "score": r["score"],
        "max_score": r["max_score"],
        "accuracy_percent": r["accuracy_percent"],
        "percentile": r["percentile"],
        "time_spent_seconds": r["time_spent_seconds"],
        "subject_breakdown": json.loads(r["subject_breakdown_json"]) if r["subject_breakdown_json"] else [],
        "solutions": json.loads(r["solutions_json"]) if r["solutions_json"] else [],
        "completed_at": r["completed_at"]
    }


# =========================================================================
# EMERGENCY MODE SESSION PERSISTENCE
# =========================================================================

def save_emergency_session(
    user_id: str,
    available_minutes: int,
    plan_data: dict,
    subject_focus: str = "all",
    exam_name: str = "",
    exam_date: str = "",
    steps_total: int = 0
) -> Dict[str, Any]:
    """Persists a new emergency study session to SQLite."""
    session_id = f"emg_{uuid.uuid4().hex[:12]}"
    now = datetime.utcnow().isoformat()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO emergency_sessions (
        id, user_id, exam_name, exam_date, available_minutes, subject_focus,
        plan_json, status, steps_completed, steps_total, topics_covered_json,
        performance_json, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, 'active', 0, ?, '[]', '{}', ?)
    """, (
        session_id, user_id, exam_name, exam_date, available_minutes,
        subject_focus, json.dumps(plan_data), steps_total, now
    ))
    conn.commit()
    conn.close()
    return {
        "id": session_id,
        "user_id": user_id,
        "status": "active",
        "created_at": now
    }


def get_emergency_session(session_id: str, user_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves an emergency session with ownership check."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM emergency_sessions WHERE id = ? AND user_id = ?
    """, (session_id, user_id))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    data = dict(row)
    data["plan"] = json.loads(data.get("plan_json", "{}"))
    data["topics_covered"] = json.loads(data.get("topics_covered_json", "[]"))
    data["performance"] = json.loads(data.get("performance_json", "{}"))
    return data


def update_emergency_session(
    session_id: str,
    user_id: str,
    status: Optional[str] = None,
    steps_completed: Optional[int] = None,
    topics_covered: Optional[List] = None,
    performance: Optional[Dict] = None
) -> Optional[Dict[str, Any]]:
    """Updates emergency session progress. Returns updated session."""
    conn = get_db_connection()
    cursor = conn.cursor()
    updates = []
    values = []
    now = datetime.utcnow().isoformat()

    if status is not None:
        updates.append("status = ?")
        values.append(status)
        if status == "completed":
            updates.append("completed_at = ?")
            values.append(now)
    if steps_completed is not None:
        updates.append("steps_completed = ?")
        values.append(steps_completed)
    if topics_covered is not None:
        updates.append("topics_covered_json = ?")
        values.append(json.dumps(topics_covered))
    if performance is not None:
        updates.append("performance_json = ?")
        values.append(json.dumps(performance))

    if not updates:
        conn.close()
        return get_emergency_session(session_id, user_id)

    values.extend([session_id, user_id])
    cursor.execute(
        f"UPDATE emergency_sessions SET {', '.join(updates)} WHERE id = ? AND user_id = ?",
        tuple(values)
    )
    conn.commit()
    conn.close()
    return get_emergency_session(session_id, user_id)


def get_user_emergency_history(user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Retrieves recent emergency sessions for a student."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, exam_name, available_minutes, subject_focus, status,
           steps_completed, steps_total, created_at, completed_at
    FROM emergency_sessions
    WHERE user_id = ?
    ORDER BY created_at DESC
    LIMIT ?
    """, (user_id, limit))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


# =========================================================================
# CLASSROOM & TEACHER MANAGEMENT
# =========================================================================

def _clean_code_chars() -> str:
    # Character set excluding 0, 1, I, O, L for maximum clarity
    return "23456789ABCDEFGHJKMNPQRSTUVWXYZ"


def generate_unique_class_code(subject: str = "") -> str:
    """
    Generates a collision-safe, human-friendly unique class code.
    Format: 3-letter subject prefix + 3-4 alphanumeric characters (e.g., PHY7K2, CHM8Q4).
    Excludes visually ambiguous characters (0/O, 1/I/L).
    Authoritatively checks Supabase PostgreSQL for uniqueness.
    """
    import random
    clean_sub = (subject or "").strip().lower()
    prefix_map = {
        "physics": "PHY",
        "math": "MTH",
        "mathematics": "MTH",
        "chemistry": "CHM",
        "chem": "CHM",
        "biology": "BIO",
        "bio": "BIO",
        "computer": "CS",
        "science": "SCI"
    }
    prefix = "CLS"
    for k, p in prefix_map.items():
        if k in clean_sub:
            prefix = p
            break

    chars = _clean_code_chars()
    suffix_len = 3 if len(prefix) == 3 else 4

    # 1. Authoritative check on Supabase PostgreSQL if configured
    try:
        from backend.services.supabase_service import get_pg_connection, is_supabase_configured
        if is_supabase_configured():
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor() as cur:
                    for _ in range(50):
                        suffix = "".join(random.choices(chars, k=suffix_len))
                        code = f"{prefix}{suffix}".upper()
                        cur.execute("SELECT 1 FROM public.classrooms WHERE UPPER(join_code) = UPPER(%s)", (code,))
                        if not cur.fetchone():
                            return code
                    return f"{prefix}{uuid.uuid4().hex[:5].upper()}"
    except Exception as e:
        logger.warning(f"[DB] Supabase check in generate_unique_class_code failed: {e}")

    # 2. Local SQLite fallback check
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        for _ in range(50):
            suffix = "".join(random.choices(chars, k=suffix_len))
            code = f"{prefix}{suffix}".upper()
            cursor.execute("SELECT 1 FROM classrooms WHERE UPPER(join_code) = ?", (code,))
            if not cursor.fetchone():
                return code
        return f"{prefix}{uuid.uuid4().hex[:5].upper()}"
    finally:
        conn.close()


def create_classroom(
    teacher_id: str,
    name: str,
    subject: str,
    grade_level: str = "Class 12",
    description: str = ""
) -> Dict[str, Any]:
    """
    Creates a new classroom owned by teacher_id with an automatically generated unique join code.
    Authoritatively stored in Supabase PostgreSQL and mirrored to local SQLite.
    """
    class_id = f"cls_{uuid.uuid4().hex[:12]}"
    join_code = generate_unique_class_code(subject)
    now = datetime.utcnow().isoformat()

    # 1. Write authoritatively to Supabase PostgreSQL
    try:
        from backend.services.supabase_service import get_pg_connection, is_supabase_configured
        if is_supabase_configured():
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor() as cur:
                    cur.execute("""
                    INSERT INTO public.classrooms (
                        id, teacher_id, name, subject, grade_level, description, join_code, status, is_active, created_at, updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, 'active', 1, NOW(), NOW())
                    RETURNING id, teacher_id, name, subject, grade_level, description, join_code, status, is_active, created_at, updated_at;
                    """, (class_id, teacher_id, name.strip(), subject.strip(), grade_level.strip(), description.strip(), join_code))
                    pg_conn.commit()
    except Exception as err:
        logger.error(f"[DB] Failed to insert classroom to Supabase: {err}")
        raise RuntimeError(f"Unable to persist classroom to Supabase Cloud: {err}")

    # 2. Mirror to SQLite for local replica
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO classrooms (id, teacher_id, name, subject, grade_level, description, join_code, is_active, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
        """, (class_id, teacher_id, name.strip(), subject.strip(), grade_level.strip(), description.strip(), join_code, now, now))
        conn.commit()
        conn.close()
    except Exception as sq_err:
        logger.warning(f"[DB] SQLite mirror for classroom failed (non-fatal): {sq_err}")

    return {
        "id": class_id,
        "teacher_id": teacher_id,
        "name": name.strip(),
        "subject": subject.strip(),
        "grade_level": grade_level.strip(),
        "description": description.strip(),
        "join_code": join_code,
        "status": "active",
        "student_count": 0,
        "is_active": 1,
        "created_at": now,
        "updated_at": now
    }


def get_teacher_classrooms(teacher_id: str) -> List[Dict[str, Any]]:
    """
    Retrieves all active classrooms created and owned by the specified teacher,
    with real-time enrolled student counts. Queries Supabase PostgreSQL authoritatively.
    """
    try:
        from backend.services.supabase_service import get_pg_connection, is_supabase_configured
        if is_supabase_configured():
            with get_pg_connection() as pg_conn:
                from psycopg2.extras import RealDictCursor
                with pg_conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("""
                    SELECT c.id, c.teacher_id, c.name, c.subject, c.grade_level, c.description,
                           c.join_code, c.status, c.is_active, c.created_at, c.updated_at,
                           COUNT(m.id) AS student_count
                    FROM public.classrooms c
                    LEFT JOIN public.classroom_members m ON c.id = m.classroom_id AND m.status = 'active'
                    WHERE c.teacher_id = %s AND c.is_active = 1
                    GROUP BY c.id
                    ORDER BY c.created_at DESC;
                    """, (teacher_id,))
                    rows = cur.fetchall()
                    result = []
                    for r in rows:
                        d = dict(r)
                        d["created_at"] = str(d["created_at"]) if d["created_at"] else ""
                        d["updated_at"] = str(d["updated_at"]) if d["updated_at"] else ""
                        result.append(d)
                    return result
    except Exception as err:
        logger.error(f"[DB] Error fetching teacher classrooms from Supabase: {err}")
        raise RuntimeError(f"Unable to load classrooms from cloud database: {err}")

    # Fallback to local SQLite
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT c.id, c.teacher_id, c.name, c.subject, c.grade_level, c.description,
           c.join_code, 'active' AS status, c.is_active, c.created_at, c.updated_at,
           COUNT(m.id) AS student_count
    FROM classrooms c
    LEFT JOIN classroom_members m ON c.id = m.classroom_id AND m.status = 'active'
    WHERE c.teacher_id = ? AND c.is_active = 1
    GROUP BY c.id
    ORDER BY c.created_at DESC
    """, (teacher_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_classroom_by_id(classroom_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a single classroom by its ID with enrolled student count from Supabase."""
    from backend.services.supabase_service import get_pg_connection, is_supabase_configured
    if is_supabase_configured():
        try:
            with get_pg_connection() as pg_conn:
                from psycopg2.extras import RealDictCursor
                with pg_conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("""
                    SELECT c.id, c.teacher_id, c.name, c.subject, c.grade_level, c.description,
                           c.join_code, c.status, c.is_active, c.created_at, c.updated_at,
                           COALESCE(p.full_name, u.full_name, 'Educator') AS teacher_name,
                           COALESCE(p.institution, u.institution, 'SikshaSaathi Faculty') AS teacher_institution,
                           COUNT(m.id) AS student_count
                    FROM public.classrooms c
                    LEFT JOIN public.classroom_members m ON c.id = m.classroom_id AND m.status = 'active'
                    LEFT JOIN public.profiles p ON c.teacher_id = p.user_id
                    LEFT JOIN public.users u ON c.teacher_id = u.id
                    WHERE c.id = %s
                    GROUP BY c.id, p.full_name, u.full_name, p.institution, u.institution;
                    """, (classroom_id,))
                    row = cur.fetchone()
                    if row:
                        d = dict(row)
                        d["created_at"] = str(d["created_at"]) if d["created_at"] else ""
                        d["updated_at"] = str(d["updated_at"]) if d["updated_at"] else ""
                        return d
                    return None
        except Exception as err:
            logger.error(f"[DB] Error fetching classroom by ID from Supabase: {err}")
            raise RuntimeError(f"Unable to load classroom from cloud database: {err}")

    # Fallback to local SQLite only when Supabase is not configured
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT c.id, c.teacher_id, c.name, c.subject, c.grade_level, c.description,
           c.join_code, 'active' AS status, c.is_active, c.created_at, c.updated_at,
           COALESCE(u.full_name, 'Educator') AS teacher_name,
           COALESCE(u.institution, 'SikshaSaathi Faculty') AS teacher_institution,
           COUNT(m.id) AS student_count
    FROM classrooms c
    LEFT JOIN classroom_members m ON c.id = m.classroom_id AND m.status = 'active'
    LEFT JOIN users u ON c.teacher_id = u.id
    WHERE c.id = ?
    GROUP BY c.id, u.full_name, u.institution
    """, (classroom_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_classroom_by_code(join_code: str) -> Optional[Dict[str, Any]]:
    """
    Case-insensitive lookup for active classrooms by public join code.
    Includes teacher display name and institution from profiles.
    """
    code_clean = (join_code or "").strip().upper()
    from backend.services.supabase_service import get_pg_connection, is_supabase_configured
    if is_supabase_configured():
        try:
            with get_pg_connection() as pg_conn:
                from psycopg2.extras import RealDictCursor
                with pg_conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("""
                    SELECT c.id, c.teacher_id, c.name, c.subject, c.grade_level, c.description,
                           c.join_code, c.status, c.is_active, c.created_at,
                           COALESCE(p.full_name, u.full_name, 'Educator') AS teacher_name,
                           COALESCE(p.institution, u.institution, '') AS teacher_institution
                    FROM public.classrooms c
                    LEFT JOIN public.profiles p ON c.teacher_id = p.user_id
                    LEFT JOIN public.users u ON c.teacher_id = u.id
                    WHERE UPPER(c.join_code) = %s AND c.is_active = 1 AND c.status = 'active';
                    """, (code_clean,))
                    row = cur.fetchone()
                    if row:
                        d = dict(row)
                        d["created_at"] = str(d["created_at"]) if d["created_at"] else ""
                        return d
                    return None
        except Exception as err:
            logger.error(f"[DB] Error querying classroom by code in Supabase: {err}")
            raise RuntimeError(f"Unable to query classroom from cloud database: {err}")

    # Fallback to local SQLite only when Supabase is not configured
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT c.id, c.teacher_id, c.name, c.subject, c.grade_level, c.description, c.join_code, 'active' AS status, c.is_active, c.created_at,
           COALESCE(u.full_name, 'Educator') AS teacher_name,
           COALESCE(u.institution, '') AS teacher_institution
    FROM classrooms c
    LEFT JOIN users u ON c.teacher_id = u.id
    WHERE UPPER(c.join_code) = UPPER(?) AND c.is_active = 1
    """, (code_clean,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def is_student_active_member(student_id: str, classroom_id: str) -> bool:
    """Checks if a student is an active enrolled member of a classroom in Supabase."""
    try:
        from backend.services.supabase_service import get_pg_connection, is_supabase_configured
        if is_supabase_configured():
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor() as cur:
                    cur.execute("""
                    SELECT 1 FROM public.classroom_members
                    WHERE classroom_id = %s AND student_id = %s AND status = 'active'
                    LIMIT 1;
                    """, (classroom_id, student_id))
                    return bool(cur.fetchone())
    except Exception as err:
        logger.warning(f"[DB] Error checking active membership in Supabase: {err}")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 1 FROM classroom_members
    WHERE classroom_id = ? AND student_id = ? AND status = 'active'
    LIMIT 1
    """, (classroom_id, student_id))
    found = bool(cursor.fetchone())
    conn.close()
    return found


def join_classroom(student_id: str, classroom_id: str) -> Dict[str, Any]:
    """
    Enrolls an authenticated student into a classroom.
    Enforces duplicate membership prevention, row-level locking, and verifies class is active.
    """
    classroom = get_classroom_by_id(classroom_id)
    if not classroom:
        return {"status": "not_found", "message": "Classroom not found."}
    if classroom.get("is_active") != 1 or classroom.get("status") == "archived":
        return {"status": "archived", "message": "This classroom is archived and no longer accepting students."}

    now = datetime.utcnow().isoformat()

    # 1. Update or Insert in Supabase PostgreSQL with transaction isolation
    try:
        from backend.services.supabase_service import get_pg_connection, is_supabase_configured
        if is_supabase_configured():
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor() as cur:
                    # Check existing membership with row locking
                    cur.execute("""
                    SELECT id, status FROM public.classroom_members
                    WHERE classroom_id = %s AND student_id = %s
                    FOR UPDATE;
                    """, (classroom_id, student_id))
                    existing = cur.fetchone()

                    if existing:
                        mem_id, mem_status = existing[0], existing[1]
                        if mem_status == "active":
                            return {
                                "status": "already_joined",
                                "message": "You are already an active member of this classroom."
                            }
                        # Re-activate previously left membership
                        cur.execute("""
                        UPDATE public.classroom_members
                        SET status = 'active', joined_at = NOW(), updated_at = NOW()
                        WHERE id = %s;
                        """, (mem_id,))
                        pg_conn.commit()
                    else:
                        # New membership insertion with conflict safety
                        cur.execute("""
                        INSERT INTO public.classroom_members (
                            classroom_id, student_id, joined_at, status, created_at, updated_at
                        ) VALUES (%s, %s, NOW(), 'active', NOW(), NOW())
                        ON CONFLICT (classroom_id, student_id)
                        DO UPDATE SET status = 'active', joined_at = NOW(), updated_at = NOW();
                        """, (classroom_id, student_id))
                        pg_conn.commit()
    except Exception as err:
        err_str = str(err).lower()
        if "unique" in err_str or "duplicate" in err_str:
            return {
                "status": "already_joined",
                "message": "You are already an active member of this classroom."
            }
        logger.error(f"[DB] Failed to save membership to Supabase: {err}")
        raise RuntimeError(f"Unable to save classroom membership to cloud database: {err}")

    # 2. Mirror to SQLite
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO classroom_members (classroom_id, student_id, joined_at, status)
        VALUES (?, ?, ?, 'active')
        ON CONFLICT(classroom_id, student_id) DO UPDATE SET status = 'active', joined_at = ?
        """, (classroom_id, student_id, now, now))
        conn.commit()
        conn.close()
    except Exception as sq_err:
        logger.warning(f"[DB] SQLite mirror for membership join failed (non-fatal): {sq_err}")

    return {
        "status": "success",
        "message": f"Successfully joined {classroom['name']}.",
        "classroom": classroom
    }


def leave_classroom(student_id: str, classroom_id: str) -> Dict[str, Any]:
    """
    Student leaves a classroom. Sets membership status to 'left'.
    PRESERVES all student learning data, quiz attempts, progress, notes, and genome.
    """
    try:
        from backend.services.supabase_service import get_pg_connection, is_supabase_configured
        if is_supabase_configured():
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor() as cur:
                    cur.execute("""
                    UPDATE public.classroom_members
                    SET status = 'left', updated_at = NOW()
                    WHERE classroom_id = %s AND student_id = %s AND status = 'active';
                    """, (classroom_id, student_id))
                    pg_conn.commit()
    except Exception as err:
        logger.error(f"[DB] Error leaving classroom in Supabase: {err}")
        raise RuntimeError(f"Unable to update classroom membership in cloud database: {err}")

    # Mirror to SQLite
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE classroom_members
        SET status = 'left'
        WHERE classroom_id = ? AND student_id = ? AND status = 'active'
        """, (classroom_id, student_id))
        conn.commit()
        conn.close()
    except Exception as sq_err:
        logger.warning(f"[DB] SQLite mirror for membership leave failed (non-fatal): {sq_err}")

    return {
        "status": "success",
        "message": "You have left the classroom. Your learning history remains safe."
    }


def get_student_classrooms(student_id: str) -> List[Dict[str, Any]]:
    """
    Returns all active classrooms joined by the student,
    with teacher profile details and subject badges.
    """
    try:
        from backend.services.supabase_service import get_pg_connection, is_supabase_configured
        if is_supabase_configured():
            with get_pg_connection() as pg_conn:
                from psycopg2.extras import RealDictCursor
                with pg_conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("""
                    SELECT c.id, c.name, c.subject, c.grade_level, c.description, c.join_code,
                           m.joined_at, m.status,
                           COALESCE(p.full_name, u.full_name, 'Educator') AS teacher_name,
                           COALESCE(p.institution, u.institution, '') AS teacher_institution,
                           COALESCE(p.avatar_url, u.avatar_url, '') AS teacher_avatar
                    FROM public.classroom_members m
                    JOIN public.classrooms c ON m.classroom_id = c.id
                    LEFT JOIN public.profiles p ON c.teacher_id = p.user_id
                    LEFT JOIN public.users u ON c.teacher_id = u.id
                    WHERE m.student_id = %s AND m.status = 'active' AND c.is_active = 1
                    ORDER BY m.joined_at DESC;
                    """, (student_id,))
                    rows = cur.fetchall()
                    result = []
                    for r in rows:
                        d = dict(r)
                        d["joined_at"] = str(d["joined_at"]) if d["joined_at"] else ""
                        result.append(d)
                    return result
    except Exception as err:
        logger.error(f"[DB] Error getting student classrooms from Supabase: {err}")
        raise RuntimeError(f"Unable to load student classrooms from cloud database: {err}")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT c.id, c.name, c.subject, c.grade_level, c.description, c.join_code,
           m.joined_at, m.status,
           COALESCE(u.full_name, 'Educator') AS teacher_name,
           COALESCE(u.institution, '') AS teacher_institution,
           COALESCE(u.avatar_url, '') AS teacher_avatar
    FROM classroom_members m
    JOIN classrooms c ON m.classroom_id = c.id
    LEFT JOIN users u ON c.teacher_id = u.id
    WHERE m.student_id = ? AND m.status = 'active' AND c.is_active = 1
    ORDER BY m.joined_at DESC
    """, (student_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def is_student_in_teacher_class(teacher_id: str, student_id: str) -> bool:
    """
    Checks if student_id is an active enrolled member in any active classroom owned by teacher_id.
    Strict privacy guard for Learning Genome and academic telemetry access.
    """
    from backend.services.supabase_service import get_pg_connection, is_supabase_configured
    if is_supabase_configured():
        try:
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor() as cur:
                    cur.execute("""
                    SELECT 1
                    FROM public.classroom_members m
                    JOIN public.classrooms c ON m.classroom_id = c.id
                    WHERE c.teacher_id = %s AND m.student_id = %s AND m.status = 'active' AND c.is_active = 1
                    LIMIT 1;
                    """, (teacher_id, student_id))
                    return bool(cur.fetchone())
        except Exception as err:
            logger.error(f"[DB] Error checking student-teacher link in Supabase: {err}")
            raise RuntimeError(f"Unable to verify student authorization from cloud database: {err}")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 1
    FROM classroom_members m
    JOIN classrooms c ON m.classroom_id = c.id
    WHERE c.teacher_id = ? AND m.student_id = ? AND m.status = 'active' AND c.is_active = 1
    LIMIT 1
    """, (teacher_id, student_id))
    found = bool(cursor.fetchone())
    conn.close()
    return found


def get_teacher_metrics(teacher_id: str) -> Dict[str, Any]:
    """
    Aggregates real-time metrics for an educator authoritatively from Supabase:
    - total active classes owned
    - total unique students enrolled across all owned classes
    - average mastery across enrolled students from telemetry
    """
    from backend.services.supabase_service import get_pg_connection, is_supabase_configured
    if is_supabase_configured():
        try:
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor() as cur:
                    cur.execute("SELECT COUNT(*) FROM public.classrooms WHERE teacher_id = %s AND is_active = 1 AND status = 'active';", (teacher_id,))
                    total_classes = cur.fetchone()[0]

                    cur.execute("""
                    SELECT COUNT(DISTINCT m.student_id)
                    FROM public.classroom_members m
                    JOIN public.classrooms c ON m.classroom_id = c.id
                    WHERE c.teacher_id = %s AND m.status = 'active' AND c.is_active = 1;
                    """, (teacher_id,))
                    total_students = cur.fetchone()[0]

                    cur.execute("""
                    SELECT AVG(t.overall_mastery_percent)
                    FROM public.user_telemetry t
                    WHERE t.user_id IN (
                        SELECT DISTINCT m.student_id
                        FROM public.classroom_members m
                        JOIN public.classrooms c ON m.classroom_id = c.id
                        WHERE c.teacher_id = %s AND m.status = 'active' AND c.is_active = 1
                    );
                    """, (teacher_id,))
                    avg_row = cur.fetchone()
                    avg_mastery = round(float(avg_row[0]), 1) if avg_row and avg_row[0] is not None else 0.0

                    return {
                        "total_classes": total_classes,
                        "total_students": total_students,
                        "average_mastery": avg_mastery
                    }
        except Exception as err:
            logger.error(f"[DB] Error fetching teacher metrics from Supabase: {err}")
            raise RuntimeError(f"Unable to load teacher metrics from cloud database: {err}")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM classrooms WHERE teacher_id = ? AND is_active = 1", (teacher_id,))
    total_classes = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(DISTINCT m.student_id)
    FROM classroom_members m
    JOIN classrooms c ON m.classroom_id = c.id
    WHERE c.teacher_id = ? AND m.status = 'active' AND c.is_active = 1
    """, (teacher_id,))
    total_students = cursor.fetchone()[0]

    cursor.execute("""
    SELECT AVG(t.overall_mastery_percent)
    FROM user_telemetry t
    WHERE t.user_id IN (
        SELECT DISTINCT m.student_id
        FROM classroom_members m
        JOIN classrooms c ON m.classroom_id = c.id
        WHERE c.teacher_id = ? AND m.status = 'active' AND c.is_active = 1
    )
    """, (teacher_id,))
    avg_mastery_row = cursor.fetchone()
    avg_mastery = round(float(avg_mastery_row[0]), 1) if avg_mastery_row and avg_mastery_row[0] is not None else 0.0
    conn.close()

    return {
        "total_classes": total_classes,
        "total_students": total_students,
        "average_mastery": avg_mastery
    }


def get_classroom_students(classroom_id: str, teacher_id: str) -> List[Dict[str, Any]]:
    """
    Returns list of enrolled students in a specific classroom owned by teacher_id from Supabase.
    """
    from backend.services.supabase_service import get_pg_connection, is_supabase_configured
    if is_supabase_configured():
        try:
            with get_pg_connection() as pg_conn:
                from psycopg2.extras import RealDictCursor
                with pg_conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("""
                    SELECT m.student_id AS id,
                           COALESCE(p.full_name, u.full_name, 'Student') AS full_name,
                           COALESCE(p.email, u.email, '') AS email,
                           COALESCE(p.avatar_url, u.avatar_url, '') AS avatar_url,
                           COALESCE(p.class_level, u.class_grade, 'Class 12') AS class_grade,
                           m.joined_at,
                           COALESCE(t.overall_mastery_percent, 0.0) AS mastery_percent,
                           COALESCE(t.active_learning_streak_days, 0) AS streak_days
                    FROM public.classroom_members m
                    JOIN public.classrooms c ON m.classroom_id = c.id
                    LEFT JOIN public.profiles p ON m.student_id = p.user_id
                    LEFT JOIN public.users u ON m.student_id = u.id
                    LEFT JOIN public.user_telemetry t ON m.student_id = t.user_id
                    WHERE m.classroom_id = %s AND c.teacher_id = %s AND m.status = 'active'
                    ORDER BY m.joined_at ASC;
                    """, (classroom_id, teacher_id))
                    rows = cur.fetchall()
                    result = []
                    for r in rows:
                        d = dict(r)
                        d["joined_at"] = str(d["joined_at"]) if d["joined_at"] else ""
                        d["name"] = d.get("full_name") or "Student"
                        d["streak"] = d.get("streak_days") or 0
                        m_pct = float(d.get("mastery_percent") or 0.0)
                        
                        # Fallback to local user_telemetry if cloud telemetry is unpopulated
                        if m_pct == 0.0:
                            try:
                                s_conn = get_db_connection()
                                s_cur = s_conn.cursor()
                                s_cur.execute("SELECT overall_mastery_percent, active_learning_streak_days FROM user_telemetry WHERE user_id = ?", (d["id"],))
                                t_row = s_cur.fetchone()
                                if t_row and t_row[0] is not None:
                                    m_pct = float(t_row[0])
                                    d["mastery_percent"] = m_pct
                                    if t_row[1] is not None and not d.get("streak"):
                                        d["streak_days"] = int(t_row[1])
                                        d["streak"] = d["streak_days"]
                                s_conn.close()
                            except Exception:
                                pass

                        if m_pct >= 85:
                            d["status_tier"] = "Excelling"
                            d["badge_class"] = "badge-emerald"
                        elif m_pct >= 70:
                            d["status_tier"] = "On Track"
                            d["badge_class"] = "badge-indigo"
                        else:
                            d["status_tier"] = "Needs Attention"
                            d["badge_class"] = "badge-rose"
                        result.append(d)
                    return result
        except Exception as err:
            logger.error(f"[DB] Error fetching classroom students from Supabase: {err}")
            raise RuntimeError(f"Unable to load classroom students from cloud database: {err}")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT u.id, u.full_name, u.email, u.class_grade, m.joined_at,
           COALESCE(t.overall_mastery_percent, 0.0) AS mastery_percent,
           COALESCE(t.active_learning_streak_days, 0) AS streak_days
    FROM classroom_members m
    JOIN users u ON m.student_id = u.id
    JOIN classrooms c ON m.classroom_id = c.id
    LEFT JOIN user_telemetry t ON u.id = t.user_id
    WHERE m.classroom_id = ? AND c.teacher_id = ? AND m.status = 'active'
    ORDER BY m.joined_at ASC
    """, (classroom_id, teacher_id))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    for r in rows:
        r["name"] = r.get("full_name") or "Student"
        r["streak"] = r.get("streak_days") or 0
        m_pct = float(r.get("mastery_percent") or 0.0)
        if m_pct >= 85:
            r["status_tier"] = "Excelling"
            r["badge_class"] = "badge-emerald"
        elif m_pct >= 70:
            r["status_tier"] = "On Track"
            r["badge_class"] = "badge-indigo"
        else:
            r["status_tier"] = "Needs Attention"
            r["badge_class"] = "badge-rose"
    return rows


def get_all_teacher_students(teacher_id: str) -> List[Dict[str, Any]]:
    """
    Retrieves all unique enrolled active students across all active classrooms owned by teacher_id from Supabase.
    Includes real telemetry mastery percent, learning streak, status tier, and enrolled class name.
    """
    from backend.services.supabase_service import get_pg_connection, is_supabase_configured
    if is_supabase_configured():
        try:
            with get_pg_connection() as pg_conn:
                from psycopg2.extras import RealDictCursor
                with pg_conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("""
                    SELECT DISTINCT ON (m.student_id)
                        m.student_id AS id,
                        COALESCE(p.full_name, u.full_name, 'Student') AS full_name,
                        COALESCE(p.email, u.email, '') AS email,
                        COALESCE(p.avatar_url, u.avatar_url, '') AS avatar_url,
                        COALESCE(p.class_level, u.class_grade, 'Class 12') AS class_grade,
                        c.name AS class_name,
                        c.id AS class_id,
                        m.joined_at,
                        COALESCE(t.overall_mastery_percent, 0.0) AS mastery_percent,
                        COALESCE(t.active_learning_streak_days, 0) AS streak_days
                    FROM public.classroom_members m
                    JOIN public.classrooms c ON m.classroom_id = c.id
                    LEFT JOIN public.profiles p ON m.student_id = p.user_id
                    LEFT JOIN public.users u ON m.student_id = u.id
                    LEFT JOIN public.user_telemetry t ON m.student_id = t.user_id
                    WHERE c.teacher_id = %s AND m.status = 'active' AND c.is_active = 1
                    ORDER BY m.student_id, m.joined_at DESC;
                    """, (teacher_id,))
                    rows = cur.fetchall()
                    result = []
                    for r in rows:
                        d = dict(r)
                        d["joined_at"] = str(d["joined_at"]) if d["joined_at"] else ""
                        d["name"] = d.get("full_name") or "Student"
                        d["streak"] = d.get("streak_days") or 0
                        m_pct = float(d.get("mastery_percent") or 0.0)
                        
                        # Fallback to local user_telemetry if cloud telemetry is unpopulated
                        if m_pct == 0.0:
                            try:
                                s_conn = get_db_connection()
                                s_cur = s_conn.cursor()
                                s_cur.execute("SELECT overall_mastery_percent, active_learning_streak_days FROM user_telemetry WHERE user_id = ?", (d["id"],))
                                t_row = s_cur.fetchone()
                                if t_row and t_row[0] is not None:
                                    m_pct = float(t_row[0])
                                    d["mastery_percent"] = m_pct
                                    if t_row[1] is not None and not d.get("streak"):
                                        d["streak_days"] = int(t_row[1])
                                        d["streak"] = d["streak_days"]
                                s_conn.close()
                            except Exception:
                                pass

                        if m_pct >= 85:
                            d["status_tier"] = "Excelling"
                            d["badge_class"] = "badge-emerald"
                        elif m_pct >= 70:
                            d["status_tier"] = "On Track"
                            d["badge_class"] = "badge-indigo"
                        else:
                            d["status_tier"] = "Needs Attention"
                            d["badge_class"] = "badge-rose"
                        result.append(d)
                    return result
        except Exception as err:
            logger.error(f"[DB] Error fetching all teacher students from Supabase: {err}")
            raise RuntimeError(f"Unable to load student roster from cloud database: {err}")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT DISTINCT m.student_id AS id,
           COALESCE(u.full_name, 'Student') AS full_name,
           COALESCE(u.email, '') AS email,
           COALESCE(u.avatar_url, '') AS avatar_url,
           COALESCE(u.class_grade, 'Class 12') AS class_grade,
           c.name AS class_name,
           c.id AS class_id,
           m.joined_at,
           COALESCE(t.overall_mastery_percent, 0.0) AS mastery_percent,
           COALESCE(t.active_learning_streak_days, 0) AS streak_days
    FROM classroom_members m
    JOIN classrooms c ON m.classroom_id = c.id
    LEFT JOIN users u ON m.student_id = u.id
    LEFT JOIN user_telemetry t ON m.student_id = t.user_id
    WHERE c.teacher_id = ? AND m.status = 'active' AND c.is_active = 1
    ORDER BY m.joined_at DESC
    """, (teacher_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    for r in rows:
        r["name"] = r.get("full_name") or "Student"
        r["streak"] = r.get("streak_days") or 0
        m_pct = float(r.get("mastery_percent") or 0.0)
        if m_pct >= 85:
            r["status_tier"] = "Excelling"
            r["badge_class"] = "badge-emerald"
        elif m_pct >= 70:
            r["status_tier"] = "On Track"
            r["badge_class"] = "badge-indigo"
        else:
            r["status_tier"] = "Needs Attention"
            r["badge_class"] = "badge-rose"
    return rows


def get_classroom_hub_data(classroom_id: str, student_id: str = None) -> Dict[str, Any]:
    """
    Returns rich, production-grade Classroom Hub data:
    - Classroom details & Teacher profile
    - Announcements ("What the teacher is saying")
    - Study Notes & Lecture Materials ("What notes he uploaded")
    - Active Assignments & Cohort Quizzes
    - Doubt Desk Q&A
    - Cohort Mastery Pulse
    """
    classroom = get_classroom_by_id(classroom_id)
    if not classroom:
        return {}

    subject = classroom.get("subject", "Physics")
    teacher_name = classroom.get("teacher_name", "Educator")

    conn = get_db_connection()
    cur = conn.cursor()

    # 1. Announcements
    cur.execute("""
    SELECT id, author_name, title, content, tag, is_pinned, created_at
    FROM classroom_announcements
    WHERE classroom_id = ?
    ORDER BY is_pinned DESC, created_at DESC
    """, (classroom_id,))
    announcements = [dict(r) for r in cur.fetchall()]

    if not announcements:
        announcements = [
            {
                "id": f"ann_{classroom_id[:6]}_1",
                "classroom_id": classroom_id,
                "author_name": teacher_name,
                "title": f"Welcome to our {classroom.get('name')} Cohort!",
                "content": f"Welcome scholars! All chapter derivations, high-yield concept maps, and practice problem sheets for {subject} will be posted here. Make sure to complete Diagnostic Assessment #1 before Friday.",
                "tag": "Important",
                "is_pinned": 1,
                "created_at": "Today"
            },
            {
                "id": f"ann_{classroom_id[:6]}_2",
                "classroom_id": classroom_id,
                "author_name": teacher_name,
                "title": f"{subject} Formula & Key Concept Notes Uploaded",
                "content": "Check the Study Notes tab above for the newly uploaded chapter formula sheet and worked numericals.",
                "tag": "Lecture Notes",
                "is_pinned": 0,
                "created_at": "Yesterday"
            },
            {
                "id": f"ann_{classroom_id[:6]}_3",
                "classroom_id": classroom_id,
                "author_name": teacher_name,
                "title": "Weekly Doubt Desk Active",
                "content": "Got stuck on derivations or numericals? Post your questions directly in the Doubt Desk tab. The AI Socratic hint engine is also enabled for after-hours study.",
                "tag": "General",
                "is_pinned": 0,
                "created_at": "2 days ago"
            }
        ]

    # 2. Materials & Uploaded Notes
    cur.execute("""
    SELECT id, subject, title, topic, file_type, read_time, summary, content, download_url, created_at
    FROM classroom_materials
    WHERE classroom_id = ?
    ORDER BY created_at DESC
    """, (classroom_id,))
    materials = [dict(r) for r in cur.fetchall()]

    if not materials:
        subj_lower = subject.lower()
        if "chem" in subj_lower:
            materials = [
                {
                    "id": "mat_chem_1",
                    "subject": "Chemistry",
                    "title": "Class 12 Organic Chemistry: Reaction Mechanisms & Reagents Cheat-Sheet",
                    "topic": "Organic Synthesis",
                    "file_type": "PDF Guide",
                    "read_time": "14 mins",
                    "summary": "Master Sn1, Sn2, E1, E2 mechanisms, named reactions (Aldol, Cannizzaro, Reimer-Tiemann) and reagent chart.",
                    "content": "### Organic Chemistry High-Yield Mechanisms\n\n#### 1. Nucleophilic Substitution (Sn1 vs Sn2)\n- **Sn1**: Two-step mechanism via carbocation intermediate. Polar protic solvents stabilize carbocation. Racemization occurs.\n- **Sn2**: Single-step concerted backside attack. Inversion of configuration (Walden inversion). Favored in polar aprotic solvents.",
                    "download_url": "#",
                    "created_at": "2 days ago"
                },
                {
                    "id": "mat_chem_2",
                    "subject": "Chemistry",
                    "title": "Chemical Kinetics & Rate Laws — NCERT Exemplar Solutions",
                    "topic": "Physical Chemistry",
                    "file_type": "Formula Matrix",
                    "read_time": "10 mins",
                    "summary": "Integrated rate equations, zero/first order half-life expressions, and Arrhenius activation energy derivations.",
                    "content": "### Chemical Kinetics Summary\n\n#### Rate Law & Order of Reaction\n- **Zero Order**: $[A] = [A]_0 - kt$, Half-life $t_{1/2} = \\frac{[A]_0}{2k}$\n- **First Order**: $\\ln[A] = \\ln[A]_0 - kt$, Half-life $t_{1/2} = \\frac{0.693}{k}$",
                    "download_url": "#",
                    "created_at": "3 days ago"
                }
            ]
        elif "bio" in subj_lower:
            materials = [
                {
                    "id": "mat_bio_1",
                    "subject": "Biology",
                    "title": "Class 12 Biology: Principles of Inheritance & Variation — Mendel's Laws",
                    "topic": "Genetics & Evolution",
                    "file_type": "Visual Guide",
                    "read_time": "16 mins",
                    "summary": "Monohybrid & dihybrid cross ratios, incomplete dominance, codominance, chromosomal theory of inheritance, and pedigree charts.",
                    "content": "### Genetics Master Notes\n\n#### 1. Mendel's Postulates\n- **Law of Dominance**: In a monohybrid cross, recessive trait remains latent in F1 generation.\n- **Law of Segregation**: Alleles separate cleanly during gametogenesis.\n- **Independent Assortment**: Dihybrid ratio 9:3:3:1.",
                    "download_url": "#",
                    "created_at": "Yesterday"
                },
                {
                    "id": "mat_bio_2",
                    "subject": "Biology",
                    "title": "Molecular Basis of Inheritance — DNA Replication & Translation Sheet",
                    "topic": "Molecular Biology",
                    "file_type": "PDF Summary",
                    "read_time": "12 mins",
                    "summary": "Meselson-Stahl experiment, DNA polymerases, transcription bubble, and genetic code properties.",
                    "content": "### Molecular Biology High-Yield Sheet\n\n- DNA Replication is semi-conservative and semi-discontinuous (Okazaki fragments).\n- Leading strand (5'->3') synthesis is continuous.",
                    "download_url": "#",
                    "created_at": "4 days ago"
                }
            ]
        elif "math" in subj_lower:
            materials = [
                {
                    "id": "mat_math_1",
                    "subject": "Mathematics",
                    "title": "Class 12 Calculus: Integration By Parts & Substitution Shortcuts",
                    "topic": "Integral Calculus",
                    "file_type": "LaTeX Formulas",
                    "read_time": "12 mins",
                    "summary": "ILATE rule, reduction formulas, standard algebraic substitutions, and definite integrals properties.",
                    "content": "### Calculus Integration Matrix\n\n$$\\int u\\,dv = uv - \\int v\\,du$$\n\nDefinite Integral Property: $\\int_0^a f(x)\\,dx = \\int_0^a f(a - x)\\,dx$",
                    "download_url": "#",
                    "created_at": "3 days ago"
                }
            ]
        else:
            materials = [
                {
                    "id": "mat_phys_1",
                    "subject": "Physics",
                    "title": "NCERT Class 12 Physics: Laws of Motion, Momentum & Friction Sheet",
                    "topic": "Mechanics",
                    "file_type": "PDF & Formulas",
                    "read_time": "14 mins",
                    "summary": "Newton's 3 Laws of Motion, free-body diagram recipes, static and kinetic friction equations, and banked road turns.",
                    "content": "### Classical Mechanics & Laws of Motion\n\n#### 1. Newton's Second Law\n$$\\vec{F}_{net} = \\frac{d\\vec{p}}{dt} = m\\vec{a}$$\n\n#### 2. Friction Mechanics\n- **Static Friction**: $f_s \\le \\mu_s N$\n- **Kinetic Friction**: $f_k = \\mu_k N$\n- **Optimum banking speed**: $v = \\sqrt{rg \\tan\\theta}$",
                    "download_url": "#",
                    "created_at": "Today"
                },
                {
                    "id": "mat_phys_2",
                    "subject": "Physics",
                    "title": "Rotational Dynamics & Moment of Inertia — Solved Problems",
                    "topic": "Rotational Motion",
                    "file_type": "Concept Sheet",
                    "read_time": "15 mins",
                    "summary": "Parallel and perpendicular axis theorems, torque $\\tau = I\\alpha$, rolling without slipping energy conservation.",
                    "content": "### Rotational Dynamics Summary\n\n- Torque: $\\vec{\\tau} = \\vec{r} \\times \\vec{F} = I\\vec{\\alpha}$\n- Angular Momentum: $\\vec{L} = I\\vec{\\omega}$\n- Kinetic Energy of Rolling: $K = \\frac{1}{2}mv^2 + \\frac{1}{2}I\\omega^2$",
                    "download_url": "#",
                    "created_at": "2 days ago"
                },
                {
                    "id": "mat_phys_3",
                    "subject": "Physics",
                    "title": "Work, Energy & Power — High-Weightage Concept Review",
                    "topic": "Work-Energy",
                    "file_type": "PDF Guide",
                    "read_time": "10 mins",
                    "summary": "Work-energy theorem $W_{net} = \\Delta K$, conservative force potentials, and power output calculations.",
                    "content": "### Work, Energy & Power\n\n$$W = \\int \\vec{F} \\cdot d\\vec{r}$$\n\nWork done by conservative force equals negative change in potential energy: $W_c = -\\Delta U$",
                    "download_url": "#",
                    "created_at": "4 days ago"
                }
            ]

    # 3. Active Assignments & Quizzes
    assignments = [
        {
            "id": f"asg_{classroom_id[:6]}_1",
            "title": f"{subject} Diagnostic Assessment #1 — Foundation",
            "subject": subject,
            "questions_count": 10,
            "duration": "15 mins",
            "due_date": "Sunday, 11:59 PM",
            "status": "Pending",
            "practice_url": f"student-practice.html?subject={subject.lower()}"
        },
        {
            "id": f"asg_{classroom_id[:6]}_2",
            "title": f"Weekly Socratic Flashcards Drill — {subject}",
            "subject": subject,
            "questions_count": 8,
            "duration": "10 mins",
            "due_date": "Daily Revision",
            "status": "Active",
            "practice_url": "student-flashcards.html"
        }
    ]

    # 4. Doubt Desk Q&A
    cur.execute("""
    SELECT id, student_name, question, topic, ai_hint, teacher_reply, status, created_at
    FROM classroom_doubts
    WHERE classroom_id = ?
    ORDER BY created_at DESC
    """, (classroom_id,))
    doubts = [dict(r) for r in cur.fetchall()]

    if not doubts:
        doubts = [
            {
                "id": "dbt_seed_1",
                "student_name": "Aarav Sharma",
                "question": "Why does kinetic friction remain independent of the surface area of contact?",
                "topic": "Friction & Forces",
                "ai_hint": "Socratic hint: Think about the microscopic contact points. If apparent area increases, what happens to the pressure at each microscopic junction?",
                "teacher_reply": "Spot-on deduction! At the microscopic scale, the actual contact area is determined by normal load divided by yield pressure, so apparent macroscopic area cancels out.",
                "status": "answered",
                "created_at": "Yesterday"
            }
        ]

    # 5. Cohort Progress Pulse
    cohort_pulse = {
        "syllabus_pace": "On Track • Chapter 4 Active",
        "active_module": f"{subject} Core Concepts",
        "cohort_mastery": 78.5,
        "completion_rate": 84,
        "next_class_date": "Thursday, 4:30 PM"
    }

    conn.close()

    return {
        "status": "success",
        "classroom": classroom,
        "announcements": announcements,
        "materials": materials,
        "assignments": assignments,
        "doubts": doubts,
        "cohort_pulse": cohort_pulse
    }


def add_classroom_doubt(
    classroom_id: str,
    student_id: str,
    student_name: str,
    question: str,
    topic: str = "General",
    ai_hint: str = None
) -> Dict[str, Any]:
    """Saves a student doubt to the classroom Q&A desk."""
    import uuid
    import datetime
    doubt_id = f"dbt_{uuid.uuid4().hex[:10]}"
    now = datetime.datetime.utcnow().strftime("%b %d, %I:%M %p")

    # Generate helpful Socratic hint if not provided
    if not ai_hint:
        ai_hint = f"✦ Socratic Assistant: While awaiting your teacher's feedback, identify what fundamental equation or conservation law applies to '{question.strip()[:60]}...'."

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO classroom_doubts (id, classroom_id, student_id, student_name, question, topic, ai_hint, status, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, 'open', ?)
    """, (doubt_id, classroom_id, student_id, student_name, question, topic, ai_hint, now))
    conn.commit()
    conn.close()

    return {
        "id": doubt_id,
        "classroom_id": classroom_id,
        "student_id": student_id,
        "student_name": student_name,
        "question": question,
        "topic": topic,
        "ai_hint": ai_hint,
        "teacher_reply": None,
        "status": "open",
        "created_at": now
    }


def get_teacher_doubts(teacher_id: str) -> List[Dict[str, Any]]:
    """
    Returns all student doubts across all classrooms owned by this teacher.
    Matches classrooms authoritatively from both Supabase and SQLite.
    """
    teacher_classes = get_teacher_classrooms(teacher_id)
    class_map = {c["id"]: c for c in teacher_classes}
    c_ids = list(class_map.keys())

    if not c_ids:
        return []

    placeholders = ",".join(["?"] * len(c_ids))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"""
    SELECT id, classroom_id, student_id, student_name, question, topic, ai_hint, teacher_reply, status, created_at, updated_at
    FROM classroom_doubts
    WHERE classroom_id IN ({placeholders})
    ORDER BY created_at DESC
    """, c_ids)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    for r in rows:
        cls_info = class_map.get(r["classroom_id"], {})
        r["class_name"] = cls_info.get("name", "Classroom")
        r["class_subject"] = cls_info.get("subject", "Academics")

    return rows


def reply_to_classroom_doubt(doubt_id: str, teacher_id: str, reply: str) -> Optional[Dict[str, Any]]:
    """
    Persists educator guidance/reply to a student doubt.
    """
    now = datetime.datetime.utcnow().strftime("%b %d, %I:%M %p")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    UPDATE classroom_doubts
    SET teacher_reply = ?, status = 'answered', updated_at = ?
    WHERE id = ?
    """, (reply.strip(), now, doubt_id))
    conn.commit()

    cur.execute("""
    SELECT id, classroom_id, student_id, student_name, question, topic, ai_hint, teacher_reply, status, created_at, updated_at
    FROM classroom_doubts
    WHERE id = ?
    """, (doubt_id,))
    row = cur.fetchone()
    conn.close()

    return dict(row) if row else None


def get_teacher_cohort_misconceptions(
    teacher_id: str,
    class_id: Optional[str] = None,
    subject: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Computes real-time cohort error rates and conceptual frontiers for enrolled students across teacher's classrooms.
    Queries from Supabase Cloud PostgreSQL with SQLite fallback.
    Returns authentic topic misconceptions, percentage error rates, affected student counts, and pedagogical recommendations.
    """
    from backend.services.supabase_service import get_pg_connection, is_supabase_configured
    from psycopg2.extras import RealDictCursor

    subj_map = {
        'physics': 'phys',
        'phys': 'phys',
        'mathematics': 'math',
        'math': 'math',
        'chemistry': 'chem',
        'chem': 'chem',
        'biology': 'bio',
        'bio': 'bio',
        'computer science': 'cs',
        'computer': 'cs',
        'cs': 'cs'
    }
    target_subj_id = None
    if subject:
        clean_s = subject.strip().lower()
        target_subj_id = subj_map.get(clean_s)
        if not target_subj_id:
            for k, v in subj_map.items():
                if k in clean_s:
                    target_subj_id = v
                    break

    # 1. Supabase Cloud PostgreSQL (Primary Source of Truth)
    if is_supabase_configured():
        try:
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor(cursor_factory=RealDictCursor) as cur:
                    if class_id:
                        cur.execute("SELECT id FROM public.classrooms WHERE teacher_id = %s AND id = %s AND is_active = 1", (teacher_id, class_id))
                    else:
                        cur.execute("SELECT id FROM public.classrooms WHERE teacher_id = %s AND is_active = 1", (teacher_id,))
                    c_rows = cur.fetchall()
                    if not c_rows:
                        return []
                    c_ids = [r["id"] for r in c_rows]

                    cur.execute("SELECT DISTINCT student_id FROM public.classroom_members WHERE classroom_id = ANY(%s) AND status = 'active'", (c_ids,))
                    s_rows = cur.fetchall()
                    if not s_rows:
                        return []
                    student_ids = [r["student_id"] for r in s_rows]
                    total_cohort_students = len(student_ids)

                    query = """
                    SELECT 
                        qa.subject_id,
                        pq.topic,
                        COUNT(*) as total_attempts,
                        SUM(CASE WHEN ans.is_correct = 0 THEN 1 ELSE 0 END) as error_count,
                        COUNT(DISTINCT ans.user_id) as total_students_attempted,
                        COUNT(DISTINCT CASE WHEN ans.is_correct = 0 THEN ans.user_id END) as affected_students_count,
                        MIN(pq.explanation) as sample_explanation,
                        MIN(pq.question_text) as sample_question
                    FROM public.quiz_answers ans
                    JOIN public.practice_questions pq ON ans.question_id = pq.id
                    JOIN public.quiz_attempts qa ON ans.attempt_id = qa.id
                    WHERE ans.user_id = ANY(%s)
                    """
                    params = [student_ids]
                    if target_subj_id:
                        query += " AND qa.subject_id = %s"
                        params.append(target_subj_id)

                    query += """
                    GROUP BY qa.subject_id, pq.topic
                    HAVING SUM(CASE WHEN ans.is_correct = 0 THEN 1 ELSE 0 END) > 0
                    ORDER BY (SUM(CASE WHEN ans.is_correct = 0 THEN 1 ELSE 0 END)::float / NULLIF(COUNT(*), 0)) DESC
                    LIMIT 20
                    """
                    cur.execute(query, tuple(params))
                    rows = cur.fetchall()

                    results = []
                    subj_display = {"phys": "Physics", "math": "Mathematics", "chem": "Chemistry", "bio": "Biology", "cs": "Computer Science"}
                    for r in rows:
                        tot = int(r["total_attempts"]) or 1
                        err_cnt = int(r["error_count"]) or 0
                        rate = round((err_cnt / tot) * 100)
                        aff = int(r["affected_students_count"]) or 1
                        risk = "CRITICAL" if rate >= 50 else ("WARNING" if rate >= 30 else "GOOD")
                        s_id = r["subject_id"]
                        topic = r["topic"] or "Core Principles"

                        desc = r.get("sample_explanation") or f"Students exhibit recurring difficulty with definition boundaries and problem setups in {topic}."
                        if len(desc) > 135:
                            desc = desc[:132] + "..."

                        if risk == "CRITICAL":
                            action = f"10-min Socratic Diagnostic Drill with pair-interaction isolation on {topic}."
                        elif risk == "WARNING":
                            action = f"Interactive visual demonstration and targeted problem set on {topic}."
                        else:
                            action = f"Routine practice refresher and milestone review on {topic}."

                        results.append({
                            "subject_id": s_id,
                            "subject": subj_display.get(s_id, s_id.capitalize()),
                            "concept": topic,
                            "desc": desc,
                            "rate": rate,
                            "error_count": err_cnt,
                            "total_attempts": tot,
                            "affectedCount": aff,
                            "totalStudents": total_cohort_students,
                            "risk": risk,
                            "action": action
                        })
                    return results
        except Exception as err:
            logger.error(f"[DB] Supabase error fetching cohort misconceptions: {err}")

    # 2. SQLite fallback
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        if class_id:
            cur.execute("SELECT id FROM classrooms WHERE teacher_id = ? AND id = ? AND is_active = 1", (teacher_id, class_id))
        else:
            cur.execute("SELECT id FROM classrooms WHERE teacher_id = ? AND is_active = 1", (teacher_id,))
        c_rows = cur.fetchall()
        if not c_rows:
            conn.close()
            return []
        c_ids = [r["id"] for r in c_rows]
        c_pl = ",".join(["?"] * len(c_ids))

        cur.execute(f"SELECT DISTINCT student_id FROM classroom_members WHERE classroom_id IN ({c_pl}) AND status = 'active'", c_ids)
        s_rows = cur.fetchall()
        if not s_rows:
            conn.close()
            return []
        student_ids = [r["student_id"] for r in s_rows]
        total_cohort_students = len(student_ids)

        s_pl = ",".join(["?"] * len(student_ids))
        query = f"""
        SELECT 
            qa.subject_id,
            pq.topic,
            COUNT(*) as total_attempts,
            SUM(CASE WHEN ans.is_correct = 0 THEN 1 ELSE 0 END) as error_count,
            COUNT(DISTINCT ans.user_id) as total_students_attempted,
            COUNT(DISTINCT CASE WHEN ans.is_correct = 0 THEN ans.user_id END) as affected_students_count,
            MIN(pq.explanation) as sample_explanation
        FROM quiz_answers ans
        JOIN practice_questions pq ON ans.question_id = pq.id
        JOIN quiz_attempts qa ON ans.attempt_id = qa.id
        WHERE ans.user_id IN ({s_pl})
        """
        params = list(student_ids)
        if target_subj_id:
            query += " AND qa.subject_id = ?"
            params.append(target_subj_id)

        query += """
        GROUP BY qa.subject_id, pq.topic
        HAVING SUM(CASE WHEN ans.is_correct = 0 THEN 1 ELSE 0 END) > 0
        ORDER BY (SUM(CASE WHEN ans.is_correct = 0 THEN 1 ELSE 0 END) * 1.0 / MAX(COUNT(*), 1)) DESC
        LIMIT 20
        """
        cur.execute(query, params)
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()

        results = []
        subj_display = {"phys": "Physics", "math": "Mathematics", "chem": "Chemistry", "bio": "Biology", "cs": "Computer Science"}
        for r in rows:
            tot = int(r["total_attempts"]) or 1
            err_cnt = int(r["error_count"]) or 0
            rate = round((err_cnt / tot) * 100)
            aff = int(r["affected_students_count"]) or 1
            risk = "CRITICAL" if rate >= 50 else ("WARNING" if rate >= 30 else "GOOD")
            s_id = r["subject_id"]
            topic = r["topic"] or "Core Principles"

            desc = r.get("sample_explanation") or f"Students exhibit frequent conceptual confusion in {topic}."
            if len(desc) > 135:
                desc = desc[:132] + "..."

            results.append({
                "subject_id": s_id,
                "subject": subj_display.get(s_id, s_id.capitalize()),
                "concept": topic,
                "desc": desc,
                "rate": rate,
                "error_count": err_cnt,
                "total_attempts": tot,
                "affectedCount": aff,
                "totalStudents": total_cohort_students,
                "risk": risk,
                "action": f"10-min Diagnostic Review Drill on {topic}."
            })
        return results
    except Exception as err:
        logger.error(f"[DB] SQLite error fetching cohort misconceptions: {err}")
        return []


def get_teacher_recent_activity(teacher_id: str, limit: int = 15) -> List[Dict[str, Any]]:
    """
    Returns verified, authentic recent student activity across the teacher's enrolled cohort:
    - Diagnostic quiz attempts completed by enrolled students
    - Student doubts asked in classrooms
    """
    activities = []
    from backend.services.supabase_service import get_pg_connection, is_supabase_configured
    from psycopg2.extras import RealDictCursor

    if is_supabase_configured():
        try:
            with get_pg_connection() as pg_conn:
                with pg_conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("""
                    SELECT DISTINCT m.student_id, COALESCE(p.full_name, u.full_name, 'Student') as student_name, c.name as class_name
                    FROM public.classroom_members m
                    JOIN public.classrooms c ON m.classroom_id = c.id
                    LEFT JOIN public.profiles p ON m.student_id = p.user_id
                    LEFT JOIN public.users u ON m.student_id = u.id
                    WHERE c.teacher_id = %s AND m.status = 'active' AND c.is_active = 1
                    """, (teacher_id,))
                    st_rows = cur.fetchall()
                    if st_rows:
                        s_map = {r["student_id"]: r for r in st_rows}
                        s_ids = list(s_map.keys())

                        cur.execute("""
                        SELECT qa.id, qa.user_id, qa.subject_id, qa.level_number, qa.score, qa.total_questions, qa.accuracy_percent, qa.completed_at
                        FROM public.quiz_attempts qa
                        WHERE qa.user_id = ANY(%s)
                        ORDER BY qa.completed_at DESC
                        LIMIT %s
                        """, (s_ids, limit))
                        attempts = cur.fetchall()
                        subj_names = {"phys": "Physics", "math": "Mathematics", "chem": "Chemistry", "bio": "Biology", "cs": "Computer Science"}
                        for a in attempts:
                            st_info = s_map.get(a["user_id"], {})
                            s_name = st_info.get("student_name", "Enrolled Student")
                            c_name = st_info.get("class_name", "Classroom")
                            s_id = a["subject_id"]
                            s_title = subj_names.get(s_id, s_id.capitalize())
                            acc = float(a["accuracy_percent"] or 0.0)
                            badge = "badge-emerald" if acc >= 80 else ("badge-indigo" if acc >= 50 else "badge-rose")
                            activities.append({
                                "type": "quiz_attempt",
                                "student_name": s_name,
                                "class_name": c_name,
                                "title": f"{s_name} completed {s_title} Level {a['level_number']}",
                                "score": f"{a['score']}/{a['total_questions']}",
                                "accuracy": f"{acc}%",
                                "badge_class": badge,
                                "created_at": str(a["completed_at"]) if a.get("completed_at") else ""
                            })

                        cur.execute("""
                        SELECT d.id, d.student_name, d.question, d.topic, d.status, d.created_at, c.name as class_name
                        FROM public.classroom_doubts d
                        JOIN public.classrooms c ON d.classroom_id = c.id
                        WHERE c.teacher_id = %s
                        ORDER BY d.created_at DESC
                        LIMIT %s
                        """, (teacher_id, limit))
                        doubts = cur.fetchall()
                        for d in doubts:
                            activities.append({
                                "type": "doubt",
                                "student_name": d["student_name"],
                                "class_name": d["class_name"],
                                "title": f"Doubt from {d['student_name']}: {d['question'][:50]}...",
                                "score": d.get("topic") or "Concept Question",
                                "accuracy": "Needs Attention" if d["status"] == "open" else "Answered",
                                "badge_class": "badge-rose" if d["status"] == "open" else "badge-emerald",
                                "created_at": str(d["created_at"])
                            })
        except Exception as err:
            logger.warning(f"[Supabase] get_teacher_recent_activity warning: {err}")

    return activities


# Initialize DB and seed baseline users & practice data when module is loaded
init_db()
seed_default_users()
seed_practice_data()
