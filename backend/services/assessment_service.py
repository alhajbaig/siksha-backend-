"""
SIKSHA SAATHI — DIAGNOSTIC ASSESSMENT & EXAM SIMULATOR SERVICE
High-fidelity exam simulation engine featuring:
1. Dynamic, unique, topic-specific question generation via DynamicQuestionEngine.
2. Authentic Gaussian CDF percentile modeling calibrated to standard national percentiles.
3. Multi-subject & single-subject benchmark tests with live proctor timer & question palette.
4. Seamless SQLite persistence linking into Learning Genome, telemetry, and Smart Revision queues.
"""

import math
import uuid
import random
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

from backend.db import (
    get_db_connection, record_assessment_attempt,
    get_user_assessment_history, get_assessment_attempt_by_id,
    get_or_create_user_telemetry
)
from backend.services.question_engine import dynamic_question_engine

logger = logging.getLogger(__name__)

# In-memory store for active assessment sessions (session_id -> { questions, user_id, assessment_id, started_at })
ACTIVE_ASSESSMENT_SESSIONS: Dict[str, Dict[str, Any]] = {}

# Catalog of Diagnostic Assessments
ASSESSMENT_CATALOG = [
    {
        "id": "jee-mock-3",
        "title": "JEE Advanced Full Diagnostic Mock #3",
        "subtitle": "Comprehensive multi-subject evaluation across Physics, Chemistry, and Mathematics.",
        "subjects": ["phys", "chem", "math"],
        "category": "multi-subject",
        "badge": "JEE ADVANCED",
        "duration_minutes": 25,
        "total_questions": 15,
        "difficulty": "Hard",
        "marking": {"correct": 4, "incorrect": -1, "unattempted": 0},
        "topics": [
            {"subject_id": "phys", "topic": "Kinematics"},
            {"subject_id": "phys", "topic": "Newton's Laws"},
            {"subject_id": "phys", "topic": "Gravitation"},
            {"subject_id": "chem", "topic": "Stoichiometry"},
            {"subject_id": "chem", "topic": "Chemical Bonding"},
            {"subject_id": "chem", "topic": "Thermodynamics"},
            {"subject_id": "math", "topic": "Calculus"},
            {"subject_id": "math", "topic": "Matrices"},
            {"subject_id": "math", "topic": "Differentiation"}
        ],
        "tags": ["Full Length", "Multi-Subject", "High Yield", "Negative Marking"]
    },
    {
        "id": "math-quadratics",
        "title": "Polynomials & Quadratic Curves",
        "subtitle": "Evaluates roots, discriminant theory, vertex formulas, and parabolic intercepts.",
        "subjects": ["math"],
        "category": "mathematics",
        "badge": "MATHEMATICS",
        "duration_minutes": 15,
        "total_questions": 10,
        "difficulty": "Medium",
        "marking": {"correct": 4, "incorrect": -1, "unattempted": 0},
        "topics": [
            {"subject_id": "math", "topic": "Algebra"},
            {"subject_id": "math", "topic": "Quadratic Inequalities"}
        ],
        "tags": ["Algebra", "Class 12", "Curve Analysis"]
    },
    {
        "id": "physics-mechanics",
        "title": "Newton's Laws & Friction Dynamics",
        "subtitle": "Free body isolation, normal forces, static/kinetic friction coefficients, and pulleys.",
        "subjects": ["phys"],
        "category": "physics",
        "badge": "PHYSICS",
        "duration_minutes": 20,
        "total_questions": 10,
        "difficulty": "Medium",
        "marking": {"correct": 4, "incorrect": -1, "unattempted": 0},
        "topics": [
            {"subject_id": "phys", "topic": "Newton's Laws"},
            {"subject_id": "phys", "topic": "Dynamics"},
            {"subject_id": "phys", "topic": "Friction"}
        ],
        "tags": ["Mechanics", "Friction", "FBD Isolation"]
    },
    {
        "id": "chem-organic",
        "title": "Organic Reaction Kinetics (SN1/SN2)",
        "subtitle": "Carbocation rearrangements, steric hindrance factors, and polar solvent effects.",
        "subjects": ["chem"],
        "category": "chemistry",
        "badge": "CHEMISTRY",
        "duration_minutes": 15,
        "total_questions": 10,
        "difficulty": "Hard",
        "marking": {"correct": 4, "incorrect": -1, "unattempted": 0},
        "topics": [
            {"subject_id": "chem", "topic": "Reaction Mechanisms"},
            {"subject_id": "chem", "topic": "Carbocation Stability"}
        ],
        "tags": ["Organic Chem", "Mechanisms", "Steric Effects"]
    },
    {
        "id": "cs-ds-algo",
        "title": "Data Structures & Algorithmic Complexity",
        "subtitle": "Big-O runtime analysis, tree traversals, dynamic programming states, and hash hashing.",
        "subjects": ["cs"],
        "category": "cs",
        "badge": "COMPUTER SCIENCE",
        "duration_minutes": 20,
        "total_questions": 10,
        "difficulty": "Medium",
        "marking": {"correct": 4, "incorrect": 0, "unattempted": 0},
        "topics": [
            {"subject_id": "cs", "topic": "Data Structures"},
            {"subject_id": "cs", "topic": "Algorithm Analysis"}
        ],
        "tags": ["Data Structures", "Algorithms", "Optimization"]
    },
    {
        "id": "math-calculus",
        "title": "Limits, Derivatives & Integrals Sprint",
        "subtitle": "L'Hopital's rule, chain rule, maximum/minimum extrema, and definite integral areas.",
        "subjects": ["math"],
        "category": "mathematics",
        "badge": "MATHEMATICS",
        "duration_minutes": 20,
        "total_questions": 10,
        "difficulty": "Hard",
        "marking": {"correct": 4, "incorrect": -1, "unattempted": 0},
        "topics": [
            {"subject_id": "math", "topic": "Calculus"},
            {"subject_id": "math", "topic": "Definite Integrals"}
        ],
        "tags": ["Calculus", "Extrema", "Definite Integrals"]
    },
    {
        "id": "physics-thermo",
        "title": "Heat, Thermodynamics & Carnot Cycles",
        "subtitle": "First and second laws of thermodynamics, adiabatic expansion, and engine efficiency.",
        "subjects": ["phys"],
        "category": "physics",
        "badge": "PHYSICS",
        "duration_minutes": 20,
        "total_questions": 10,
        "difficulty": "Medium",
        "marking": {"correct": 4, "incorrect": -1, "unattempted": 0},
        "topics": [
            {"subject_id": "phys", "topic": "Thermodynamics"},
            {"subject_id": "phys", "topic": "Carnot Engine"}
        ],
        "tags": ["Thermodynamics", "PV Work", "Entropy"]
    },
    {
        "id": "chem-bonding",
        "title": "Chemical Bonding & Molecular Orbitals",
        "subtitle": "VSEPR geometries, dipole moments, MOT bond order, and hybridization states.",
        "subjects": ["chem"],
        "category": "chemistry",
        "badge": "CHEMISTRY",
        "duration_minutes": 15,
        "total_questions": 10,
        "difficulty": "Medium",
        "marking": {"correct": 4, "incorrect": -1, "unattempted": 0},
        "topics": [
            {"subject_id": "chem", "topic": "Chemical Bonding"},
            {"subject_id": "chem", "topic": "Molecular Geometry"}
        ],
        "tags": ["Inorganic Chem", "MOT", "VSEPR"]
    }
]


class AssessmentService:
    def __init__(self):
        pass

    def _normalize_subject(self, s: str) -> str:
        s_low = s.lower().strip()
        if s_low in ("physics", "phys"): return "phys"
        if s_low in ("chemistry", "chem"): return "chem"
        if s_low in ("mathematics", "math"): return "math"
        if s_low in ("computer_science", "cs"): return "cs"
        return s_low

    def _calculate_gaussian_percentile(self, accuracy_percent: float) -> float:
        """
        Calculates authentic Gaussian Cumulative Distribution Function (CDF) percentile.
        Standard aspirant distribution: Mean = 45%, Std Dev = 18%.
        Bounds results realistically between 50.0%ile and 99.9%ile.
        """
        mean = 45.0
        std_dev = 18.0
        z = (accuracy_percent - mean) / std_dev
        cdf = 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
        percentile = round(cdf * 100.0, 1)
        return max(50.0, min(99.9, percentile))

    async def get_catalog(self, user_id: str) -> Dict[str, Any]:
        """Returns catalog of all diagnostic tests enriched with user history and predicted percentile."""
        history = get_user_assessment_history(user_id)
        history_by_asmt = {}
        for item in history:
            asmt_id = item["assessment_id"]
            if asmt_id not in history_by_asmt:
                history_by_asmt[asmt_id] = item

        telemetry = get_or_create_user_telemetry(user_id)
        mastery = telemetry.get("mastery_score", 85.0)
        predicted_percentile = self._calculate_gaussian_percentile(mastery)

        catalog_enriched = []
        for test in ASSESSMENT_CATALOG:
            item = dict(test)
            last_attempt = history_by_asmt.get(test["id"])
            if last_attempt:
                item["last_attempt"] = {
                    "attempt_id": last_attempt["id"],
                    "score": last_attempt["score"],
                    "max_score": last_attempt["max_score"],
                    "accuracy_percent": last_attempt["accuracy_percent"],
                    "percentile": last_attempt["percentile"],
                    "completed_at": last_attempt["completed_at"]
                }
            else:
                item["last_attempt"] = None
            catalog_enriched.append(item)

        return {
            "predicted_percentile": predicted_percentile,
            "total_assessments": len(catalog_enriched),
            "completed_count": len(history_by_asmt),
            "assessments": catalog_enriched
        }

    async def start_assessment(self, assessment_id: str, user_id: str) -> Dict[str, Any]:
        """
        Creates an active assessment session with dynamically synthesized or curated questions.
        Sanitizes questions to exclude correct_option and explanation for true test security.
        """
        test_def = next((t for t in ASSESSMENT_CATALOG if t["id"] == assessment_id), None)
        if not test_def:
            raise ValueError(f"Assessment '{assessment_id}' not found.")

        session_id = f"asmt_sess_{uuid.uuid4().hex[:12]}"
        total_questions = test_def["total_questions"]
        topics_list = test_def["topics"]

        conn = get_db_connection()
        cursor = conn.cursor()

        # Find questions the user answered recently
        answered_ids = set()
        if user_id:
            cursor.execute("""
            SELECT question_id FROM quiz_answers WHERE user_id = ?
            ORDER BY id DESC LIMIT 50
            """, (user_id,))
            answered_ids = {r[0] for r in cursor.fetchall()}

        all_raw_questions: List[Dict[str, Any]] = []
        needed_per_topic = max(1, math.ceil(total_questions / max(len(topics_list), 1)))

        for t_spec in topics_list:
            s_id = self._normalize_subject(t_spec["subject_id"])
            t_name = t_spec["topic"]

            cursor.execute("""
            SELECT id, subject_id, level_number, topic, difficulty,
                   question_text, option_a, option_b, option_c, option_d,
                   correct_option, explanation
            FROM practice_questions
            WHERE subject_id = ? AND (topic = ? OR topic LIKE ?)
            ORDER BY RANDOM() LIMIT ?
            """, (s_id, t_name, f"%{t_name}%", needed_per_topic + 2))
            rows = [dict(r) for r in cursor.fetchall()]

            # Prioritize unattempted questions
            unattempted = [r for r in rows if r["id"] not in answered_ids]
            chosen_rows = unattempted if len(unattempted) >= needed_per_topic else rows

            for r in chosen_rows[:needed_per_topic]:
                all_raw_questions.append({
                    "id": r["id"],
                    "subject_id": r["subject_id"],
                    "topic": r["topic"],
                    "difficulty": r["difficulty"],
                    "question_text": r["question_text"],
                    "options": [
                        {"index": 0, "text": r["option_a"]},
                        {"index": 1, "text": r["option_b"]},
                        {"index": 2, "text": r["option_c"]},
                        {"index": 3, "text": r["option_d"]},
                    ],
                    "correct_option": r["correct_option"],
                    "explanation": r["explanation"]
                })

        conn.close()

        # If pool is smaller than required questions, synthesize fresh questions via DynamicQuestionEngine
        if len(all_raw_questions) < total_questions:
            deficit = total_questions - len(all_raw_questions)
            fallback_subject = self._normalize_subject(topics_list[0]["subject_id"])
            fallback_topic = topics_list[0]["topic"]
            new_qs = await dynamic_question_engine.generate_ai_questions(
                fallback_subject, fallback_topic, count=max(deficit, 3)
            )
            dynamic_question_engine.save_questions_to_db(new_qs)
            for q in new_qs[:deficit]:
                all_raw_questions.append({
                    "id": q["id"],
                    "subject_id": q["subject_id"],
                    "topic": q["topic"],
                    "difficulty": q.get("difficulty", "Medium"),
                    "question_text": q["question_text"],
                    "options": [
                        {"index": 0, "text": q["option_a"]},
                        {"index": 1, "text": q["option_b"]},
                        {"index": 2, "text": q["option_c"]},
                        {"index": 3, "text": q["option_d"]},
                    ],
                    "correct_option": q["correct_option"],
                    "explanation": q["explanation"]
                })

        # Truncate to exact count and shuffle
        if len(all_raw_questions) > total_questions:
            all_raw_questions = random.sample(all_raw_questions, total_questions)
        random.shuffle(all_raw_questions)

        # Store full questions in memory cache for scoring
        ACTIVE_ASSESSMENT_SESSIONS[session_id] = {
            "session_id": session_id,
            "user_id": user_id,
            "assessment_id": assessment_id,
            "test_def": test_def,
            "questions": all_raw_questions,
            "started_at": datetime.utcnow().isoformat()
        }

        # Build sanitized client questions payload (no correct_option, no explanation)
        client_questions = []
        for idx, q in enumerate(all_raw_questions):
            opts = list(q.get("options", []))
            client_questions.append({
                "index": idx + 1,
                "question_id": q["id"],
                "subject_id": q.get("subject_id", "physics"),
                "topic": q["topic"],
                "difficulty": q.get("difficulty", "Medium"),
                "question_text": q["question_text"],
                "options": [
                    {"index": o.get("index", i), "label": chr(65 + i), "text": o.get("text", "")}
                    for i, o in enumerate(opts)
                ]
            })

        return {
            "session_id": session_id,
            "assessment_id": assessment_id,
            "title": test_def["title"],
            "subtitle": test_def["subtitle"],
            "duration_seconds": test_def["duration_minutes"] * 60,
            "marking": test_def["marking"],
            "total_questions": len(client_questions),
            "questions": client_questions
        }

    async def submit_assessment(
        self,
        assessment_id: str,
        session_id: str,
        answers: Dict[str, Any],  # question_id -> selected_option_index (or None)
        time_spent_seconds: int,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Evaluates assessment submission, computes score, accuracy, Gaussian percentile,
        subject breakdown, and persists to SQLite database.
        """
        session = ACTIVE_ASSESSMENT_SESSIONS.get(session_id)
        test_def = next((t for t in ASSESSMENT_CATALOG if t["id"] == assessment_id), None)
        if not test_def:
            raise ValueError(f"Assessment '{assessment_id}' not found.")

        # Fallback if session expired from memory: fetch questions from DB
        raw_questions = session.get("questions") if session else []
        if not raw_questions and answers:
            q_ids = list(answers.keys())
            conn = get_db_connection()
            cursor = conn.cursor()
            placeholders = ",".join("?" for _ in q_ids)
            cursor.execute(f"""
            SELECT id, subject_id, level_number, topic, difficulty, question_text,
                   option_a, option_b, option_c, option_d, correct_option, explanation
            FROM practice_questions
            WHERE id IN ({placeholders})
            """, q_ids)
            db_rows = [dict(r) for r in cursor.fetchall()]
            conn.close()
            raw_questions = dynamic_question_engine._format_questions(db_rows)

        # Scoring & Evaluation
        marking = test_def["marking"]
        pos_mark = marking.get("correct", 4)
        neg_mark = marking.get("incorrect", -1)

        total_questions = len(raw_questions)
        attempted_count = 0
        correct_count = 0
        incorrect_count = 0
        raw_score = 0
        max_score = total_questions * pos_mark

        subject_stats: Dict[str, Dict[str, Any]] = {}
        topic_performance: Dict[str, Dict[str, Any]] = {}
        solutions: List[Dict[str, Any]] = []

        for q in raw_questions:
            q_id = q["id"]
            subj_id = q.get("subject_id", "physics")
            topic = q.get("topic", "General")
            correct_opt = q.get("correct_option", 0)

            # Initialize subject stats
            if subj_id not in subject_stats:
                subject_stats[subj_id] = {
                    "subject": subj_id.replace("_", " ").title(),
                    "total": 0,
                    "attempted": 0,
                    "correct": 0,
                    "score": 0
                }
            subject_stats[subj_id]["total"] += 1

            # Initialize topic performance
            if topic not in topic_performance:
                topic_performance[topic] = {"subject_id": subj_id, "correct": 0, "total": 0}
            topic_performance[topic]["total"] += 1

            selected_val = answers.get(q_id)
            is_attempted = selected_val is not None and str(selected_val).isdigit()

            if is_attempted:
                attempted_count += 1
                subject_stats[subj_id]["attempted"] += 1
                selected_opt = int(selected_val)
                is_correct = (selected_opt == correct_opt)

                if is_correct:
                    correct_count += 1
                    raw_score += pos_mark
                    subject_stats[subj_id]["correct"] += 1
                    subject_stats[subj_id]["score"] += pos_mark
                    topic_performance[topic]["correct"] += 1
                else:
                    incorrect_count += 1
                    raw_score += neg_mark
                    subject_stats[subj_id]["score"] += neg_mark
            else:
                selected_opt = -1
                is_correct = False

            # Extract options list for solutions
            opts = q.get("options", [])
            options_text = [o.get("text", "") for o in opts] if opts else []

            solutions.append({
                "question_id": q_id,
                "subject_id": subj_id,
                "topic": topic,
                "difficulty": q.get("difficulty", "Medium"),
                "question_text": q.get("question_text", ""),
                "options": options_text,
                "selected_option": selected_opt,
                "correct_option": correct_opt,
                "is_correct": is_correct,
                "is_attempted": is_attempted,
                "explanation": q.get("explanation", "Step-by-step analytical derivation.")
            })

        # Calculations
        raw_score = max(0, raw_score)  # Bounded at 0 minimum
        accuracy_percent = round((correct_count / max(attempted_count, 1)) * 100.0, 1) if attempted_count > 0 else 0.0
        percentile = self._calculate_gaussian_percentile(accuracy_percent)

        # Subject breakdown array
        subject_breakdown = []
        for s_id, s_data in subject_stats.items():
            tot = s_data["total"]
            corr = s_data["correct"]
            subject_breakdown.append({
                "subject_id": s_id,
                "subject": s_data["subject"],
                "total": tot,
                "attempted": s_data["attempted"],
                "correct": corr,
                "accuracy": round((corr / max(s_data["attempted"], 1)) * 100.0, 1) if s_data["attempted"] > 0 else 0.0,
                "score": max(0, s_data["score"])
            })

        # Identify strengths & weaknesses
        strong_topics = [
            t for t, d in topic_performance.items()
            if (d["correct"] / max(d["total"], 1)) >= 0.7 and d["total"] > 0
        ]
        weak_topics = [
            t for t, d in topic_performance.items()
            if (d["correct"] / max(d["total"], 1)) < 0.7 and d["total"] > 0
        ]

        attempt_id = f"asmt_att_{uuid.uuid4().hex[:12]}"

        # Persist to SQLite
        saved_record = record_assessment_attempt(
            attempt_id=attempt_id,
            user_id=user_id,
            assessment_id=assessment_id,
            title=test_def["title"],
            score=raw_score,
            max_score=max_score,
            accuracy_percent=accuracy_percent,
            percentile=percentile,
            time_spent_seconds=time_spent_seconds,
            subject_breakdown=subject_breakdown,
            solutions=solutions
        )

        # Clear session from memory
        ACTIVE_ASSESSMENT_SESSIONS.pop(session_id, None)

        return {
            "attempt_id": attempt_id,
            "assessment_id": assessment_id,
            "title": test_def["title"],
            "score": raw_score,
            "max_score": max_score,
            "accuracy_percent": accuracy_percent,
            "percentile": percentile,
            "time_spent_seconds": time_spent_seconds,
            "total_questions": total_questions,
            "attempted_count": attempted_count,
            "correct_count": correct_count,
            "incorrect_count": incorrect_count,
            "skipped_count": total_questions - attempted_count,
            "subject_breakdown": subject_breakdown,
            "strong_topics": strong_topics,
            "weak_topics": weak_topics,
            "solutions": solutions,
            "completed_at": saved_record["completed_at"]
        }

    async def get_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Returns all past assessment records for user."""
        return get_user_assessment_history(user_id)

    async def get_attempt_detail(self, attempt_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Returns full diagnostic attempt details including solutions."""
        return get_assessment_attempt_by_id(attempt_id, user_id)


assessment_service = AssessmentService()
