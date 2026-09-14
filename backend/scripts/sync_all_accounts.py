"""
SIKSHASAATHI — Comprehensive Account Synchronization Script
Migrates all local SQLite users, credentials, and profiles into Supabase Cloud PostgreSQL,
resolving all email discrepancies and ensuring 100% cloud persistence.
"""

import os
import sys
import sqlite3
from datetime import datetime

# Set module root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.services.supabase_service import get_pg_connection, is_supabase_configured

def sync_accounts():
    print("=" * 65)
    print("SIKSHASAATHI: MIGRATING ALL ACCOUNTS TO SUPABASE POSTGRESQL")
    print("=" * 65)

    if not is_supabase_configured():
        print("[ERROR] Supabase is not configured in .env!")
        return False

    db_path = os.path.join(os.path.dirname(__file__), "..", "data", "siksha_saathi.db")
    if not os.path.exists(db_path):
        print(f"[ERROR] SQLite DB not found at {db_path}")
        return False

    sqlite_conn = sqlite3.connect(db_path)
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cur = sqlite_conn.cursor()

    sqlite_cur.execute("SELECT * FROM users")
    sqlite_users = [dict(r) for r in sqlite_cur.fetchall()]
    print(f"[SQLite] Found {len(sqlite_users)} user accounts in SQLite database.")

    sqlite_cur.execute("SELECT * FROM profiles")
    sqlite_profiles = {r["user_id"]: dict(r) for r in sqlite_cur.fetchall()}

    sqlite_conn.close()

    success_count = 0
    with get_pg_connection() as pg_conn:
        with pg_conn.cursor() as pg_cur:
            for u in sqlite_users:
                u_id = u["id"]
                email = u["email"].strip().lower()
                pw_hash = u["password_hash"]
                salt = u["salt"]
                name = u["full_name"]
                role = (u.get("role") or "student").lower()
                grade = u.get("class_grade") or "Class 12 • Senior Secondary"
                goal = u.get("target_goal") or "JEE / NEET"
                inst = u.get("institution") or ""
                subj = u.get("subject") or ""
                bio = u.get("bio") or ""
                avatar = u.get("avatar_url") or ""

                # 1. Check if user already exists in Supabase by ID or Email
                pg_cur.execute("SELECT id, email FROM public.users WHERE id = %s OR email = %s;", (u_id, email))
                existing = pg_cur.fetchone()

                if existing:
                    ex_id, ex_email = existing[0], existing[1]
                    # Update existing record
                    pg_cur.execute("""
                    UPDATE public.users SET
                        email = %s,
                        password_hash = CASE WHEN %s != '' THEN %s ELSE password_hash END,
                        salt = CASE WHEN %s != '' THEN %s ELSE salt END,
                        full_name = %s,
                        role = %s,
                        class_grade = %s,
                        target_goal = %s,
                        institution = %s,
                        subject = %s,
                        bio = %s,
                        avatar_url = %s,
                        updated_at = NOW()
                    WHERE id = %s;
                    """, (
                        email, pw_hash, pw_hash, salt, salt, name, role,
                        grade, goal, inst, subj, bio, avatar, ex_id
                    ))
                    print(f"  [UPDATED] Supabase user: {email} (ID: {ex_id})")
                else:
                    # Insert new record with conflict safety
                    pg_cur.execute("""
                    INSERT INTO public.users (
                        id, email, password_hash, salt, full_name, role,
                        class_grade, target_goal, institution, subject, bio, avatar_url,
                        created_at, updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                    ON CONFLICT (email) DO UPDATE SET
                        password_hash = EXCLUDED.password_hash,
                        salt = EXCLUDED.salt,
                        full_name = EXCLUDED.full_name,
                        role = EXCLUDED.role,
                        updated_at = NOW();
                    """, (
                        u_id, email, pw_hash, salt, name, role,
                        grade, goal, inst, subj, bio, avatar
                    ))
                    print(f"  [INSERTED] Supabase user: {email} (ID: {u_id})")

                # 2. Sync profile record
                prof = sqlite_profiles.get(u_id) or {}
                prof_id = prof.get("id") or f"prof_{u_id[4:] if u_id.startswith('usr_') else u_id}"

                pg_cur.execute("""
                INSERT INTO public.profiles (
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
                    updated_at = NOW();
                """, (
                    prof_id, u_id, name, email, avatar,
                    grade, subj or "Physics", goal, inst, bio
                ))

                success_count += 1

            pg_conn.commit()

    print("=" * 65)
    print(f"SUCCESS: Synchronized {success_count}/{len(sqlite_users)} accounts into Supabase Cloud PostgreSQL!")
    print("=" * 65)
    return True

if __name__ == "__main__":
    sync_accounts()
