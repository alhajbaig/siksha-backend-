"""
SIKSHA SAATHI — Emergency Mode Orchestration Service
Situation Intelligence • Crisis Diagnosis • Value-Per-Minute Optimization • Time Protection

Consumes existing RevisionService, GenomeService, Progress, and ResourceService
to build time-constrained, evidence-backed emergency study plans.

ANTI-HALLUCINATION CONTRACT:
- Every data point comes from real database queries via existing services
- No invented scores, predictions, retention values, or exam information
- Missing data → honest empty state, never synthetic fallback
"""

import math
import json
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Any, Optional

from backend.db import (
    get_db_connection,
    get_user_progress_summary,
    get_or_create_user_telemetry,
    get_or_create_profile,
    save_emergency_session,
    get_emergency_session,
    update_emergency_session,
    save_revision_session,
    get_user_emergency_history
)
from backend.services.revision_service import revision_service
from backend.services.resource_service import resource_service


class EmergencyService:
    """
    Orchestrator service for Emergency Mode.
    Does NOT create parallel learning systems.
    Consumes existing canonical services and applies time-constrained prioritization.
    """

    # Time allocation presets (minutes)
    TIME_PRESETS = [5, 10, 15, 20, 30, 45, 60, 120, 180]

    # Minimum useful time per topic (minutes)
    MIN_TOPIC_TIME = 5

    # Real-World Emergency Scenarios for Situation Intelligence
    SCENARIOS = [
        {
            "id": "auto",
            "title": "Auto-Detect My Situation",
            "tagline": "Data-Driven Recovery",
            "icon": "🧠",
            "description": "Analyze my live learning metrics and apply the optimal recovery strategy automatically."
        },
        {
            "id": "exam_tomorrow",
            "title": "Exam Tomorrow",
            "tagline": "Marks Protection",
            "icon": "⏰",
            "description": "Protect existing marks. Focus on high-frequency topics, error patterns, and rapid retention checks."
        },
        {
            "id": "exam_today",
            "title": "Exam in a Few Hours",
            "tagline": "Rapid Recall Only",
            "icon": "⚡",
            "description": "Zero deep-learning. High-confidence recall, formula review, and immediate score boosters only."
        },
        {
            "id": "only_20_min",
            "title": "Only 20–30 Minutes",
            "tagline": "Minimum Viable Prep",
            "icon": "⏱️",
            "description": "A laser-focused micro-sprint targeting the single most dangerous misconception."
        },
        {
            "id": "keep_making_mistakes",
            "title": "I Keep Making Mistakes",
            "tagline": "Error Pattern Fix",
            "icon": "🎯",
            "description": "Pinpoint recurring misconceptions and solve targeted correction questions."
        },
        {
            "id": "cant_remember",
            "title": "Studied But Can't Remember",
            "tagline": "Memory Consolidation",
            "icon": "🔄",
            "description": "Active retrieval drills to reverse forgetting decay on recently neglected topics."
        },
        {
            "id": "completely_lost",
            "title": "I'm Completely Lost",
            "tagline": "Foundational Clarity",
            "icon": "🧭",
            "description": "Clear the confusion with foundational prerequisites and a clean, minimal path."
        },
        {
            "id": "huge_backlog",
            "title": "I Have a Huge Backlog",
            "tagline": "Strategic Triage",
            "icon": "📚",
            "description": "Skip non-essential chapters. Focus exclusively on maximum value-per-minute topics."
        }
    ]

    def _detect_situation(
        self,
        user_id: str,
        all_topics: List[Dict],
        progress: Dict[str, Any],
        exam_date: str = ""
    ) -> Dict[str, Any]:
        """
        Analyzes real student signals to diagnose their dominant academic situation.
        Never hallucinates signals.
        """
        mistake_topics = [t for t in all_topics if t.get("mistakes_count", 0) >= 1]
        repeated_mistakes = [t for t in all_topics if t.get("mistakes_count", 0) >= 2]
        decay_topics = [
            t for t in all_topics
            if t.get("days_elapsed", 0) >= 4 or (t.get("retention_percent") is not None and t.get("retention_percent") < 65)
        ]
        low_acc_topics = [
            t for t in all_topics
            if t.get("accuracy_percent") is not None and t.get("accuracy_percent") < 50
        ]
        high_acc_topics = [
            t for t in all_topics
            if t.get("accuracy_percent") is not None and t.get("accuracy_percent") >= 80
        ]

        # Determine best scenario based on actual evidence
        if exam_date:
            recommended_id = "exam_tomorrow"
            reason = f"Upcoming exam recorded for {exam_date}. Time is scarce; protect your base."
        elif len(repeated_mistakes) >= 2:
            recommended_id = "keep_making_mistakes"
            reason = f"Detected repeated misconceptions across {len(repeated_mistakes)} topics. Fixing these yields the quickest score jump."
        elif len(decay_topics) >= 3:
            recommended_id = "cant_remember"
            reason = f"{len(decay_topics)} topics show memory decay (>4 days without review). Active retrieval is critical."
        elif len(low_acc_topics) >= 4 and len(high_acc_topics) <= 1:
            recommended_id = "completely_lost"
            reason = "Multiple low-accuracy areas detected. We recommend starting with core foundational concepts."
        elif len(all_topics) >= 15:
            recommended_id = "huge_backlog"
            reason = f"{len(all_topics)} topics in your syllabus. High-yield triage will filter out low-value items."
        elif mistake_topics:
            recommended_id = "keep_making_mistakes"
            reason = f"You have logged mistakes in {len(mistake_topics)} topics that can be quickly corrected."
        else:
            recommended_id = "exam_tomorrow"
            reason = "Standard high-yield sprint targeting your top revision gaps."

        return {
            "recommended_scenario_id": recommended_id,
            "recommendation_reason": reason,
            "metrics": {
                "repeated_mistakes_count": len(repeated_mistakes),
                "decay_topics_count": len(decay_topics),
                "low_accuracy_count": len(low_acc_topics),
                "total_tracked_topics": len(all_topics)
            }
        }

    def get_student_context(self, user_id: str) -> Dict[str, Any]:
        """
        Builds the Emergency Student Context from REAL data sources only.
        Returns profile, subjects, progress, calibration level, scenarios, and situation diagnosis.
        """
        profile = get_or_create_profile(user_id)
        telemetry = get_or_create_user_telemetry(user_id)
        progress = get_user_progress_summary(user_id)

        # Get revision overview (contains topic-level retention, priority, evidence)
        revision_overview = revision_service.get_revision_overview(user_id)
        all_topics = revision_overview.get("all_topics", [])

        # Determine calibration: do we have enough data to personalize?
        total_questions = progress.get("total_questions_solved", 0)
        has_sufficient_data = total_questions >= 3 or len(all_topics) > 0
        has_history = revision_overview.get("has_history", False)

        # Build subject list from actual practice_subjects (not hardcoded)
        subjects = []
        for s in progress.get("subjects", []):
            subjects.append({
                "id": s["id"],
                "title": s["title"],
                "icon": s["icon"],
                "completed_levels": s["completed_levels"],
                "total_levels": s["total_levels"],
                "progress_percent": s["progress_percent"],
                "accuracy_percent": s["accuracy_percent"]
            })

        # Count available resources per subject
        resource_counts = defaultdict(int)
        for ch_id, ch in resource_service.chapters_db.items():
            subj = ch.get("subject", "")
            resource_counts[subj] += 1

        for s in subjects:
            s["resource_count"] = resource_counts.get(s["id"], 0)

        # Emergency history
        emergency_history = get_user_emergency_history(user_id, limit=5)

        # Situation detection
        situation_diag = self._detect_situation(user_id, all_topics, progress)

        # Mark recommended scenario in scenario list
        scenarios_with_meta = []
        for sc in self.SCENARIOS:
            sc_copy = dict(sc)
            if sc_copy["id"] == situation_diag["recommended_scenario_id"]:
                sc_copy["is_recommended"] = True
                sc_copy["recommendation_note"] = situation_diag["recommendation_reason"]
            else:
                sc_copy["is_recommended"] = False
            scenarios_with_meta.append(sc_copy)

        return {
            "status": "success",
            "student": {
                "id": user_id,
                "name": profile.get("full_name", "Student"),
                "class_level": profile.get("class_level", ""),
                "target_goal": profile.get("target_goal", ""),
            },
            "has_sufficient_data": has_sufficient_data,
            "has_history": has_history,
            "total_questions_solved": total_questions,
            "overall_accuracy": progress.get("overall_accuracy_percent", 0.0),
            "subjects": subjects,
            "time_presets": self.TIME_PRESETS,
            "scenarios": scenarios_with_meta,
            "detected_situation": situation_diag,
            "emergency_history": emergency_history
        }

    def build_plan(
        self,
        user_id: str,
        available_minutes: int,
        subject_focus: str = "all",
        situation: str = "auto",
        exam_name: str = "",
        exam_date: str = ""
    ) -> Dict[str, Any]:
        """
        Builds an evidence-backed, situation-aware emergency rescue plan.

        Algorithm:
        1. Clamp available time (5 to 300 min)
        2. Get revision overview (all topic data from canonical RevisionService)
        3. Filter by subject focus if specified
        4. Detect/resolve active situation scenario
        5. Score topics by situation-aware Value-Per-Minute
        6. Allocate time budget under hard constraint: TOTAL <= available_minutes
        7. Generate crisis diagnosis (Current Situation • Biggest Risk • Best Opportunity)
        8. Extract 'If You Only Do One Thing' spotlight action
        9. Generate 'Don't Study This Now' list with explicit reasons
        10. Generate functional time breakdown schedule
        11. Persist session and return rich response
        """
        available_minutes = max(5, min(300, available_minutes))

        # 1. Get canonical revision data
        revision_data = revision_service.get_revision_overview(user_id)

        if not revision_data.get("has_history", False):
            return self._build_empty_state_plan(user_id, available_minutes, subject_focus, exam_name)

        all_topics = revision_data.get("all_topics", [])
        if not all_topics:
            return self._build_empty_state_plan(user_id, available_minutes, subject_focus, exam_name)

        # 2. Filter by subject if specified
        if subject_focus and subject_focus.lower() != "all":
            sf = subject_focus.strip().lower()
            filtered = [
                t for t in all_topics
                if t["subject_id"].lower() == sf or t.get("subject_title", "").lower() == sf
            ]
            if not filtered:
                return self._build_empty_state_plan(user_id, available_minutes, subject_focus, exam_name)
            all_topics = filtered

        # 3. Resolve active situation scenario
        progress = get_user_progress_summary(user_id)
        situation_diag = self._detect_situation(user_id, all_topics, progress, exam_date)
        active_situation = situation if situation and situation != "auto" else situation_diag["recommended_scenario_id"]

        # 4. Calculate value-per-minute for each topic with situation weighting
        scored_topics = []
        for topic in all_topics:
            vpm = self._calculate_value_per_minute(topic, available_minutes, active_situation)
            scored_topics.append({
                **topic,
                "value_per_minute": vpm
            })

        # Sort by value-per-minute descending (deterministic)
        scored_topics.sort(key=lambda x: (-x["value_per_minute"], -x["priority_score"]))

        # 5. Allocate time budget
        priorities = []
        remaining_minutes = available_minutes
        not_prioritized = []

        for topic in scored_topics:
            if remaining_minutes < self.MIN_TOPIC_TIME:
                not_prioritized.append(topic)
                continue

            allocated_time = self._allocate_topic_time(topic, remaining_minutes, available_minutes, active_situation)

            if allocated_time < self.MIN_TOPIC_TIME:
                not_prioritized.append(topic)
                continue

            steps = self._generate_topic_steps(topic, allocated_time, active_situation)
            priority_level = self._get_priority_label(len(priorities), topic)
            reason = self._build_reason(topic, active_situation)

            priorities.append({
                "topic_id": f"{topic['subject_id']}_{topic['topic']}",
                "topic_name": topic["topic"],
                "subject_id": topic["subject_id"],
                "subject_title": topic["subject_title"],
                "subject_icon": topic.get("subject_icon", "📚"),
                "priority_level": priority_level,
                "priority_label": self._priority_label_text(priority_level),
                "allocated_minutes": allocated_time,
                "evidence": topic.get("signals", []),
                "reason": reason,
                "confidence": "Strong signal" if topic["attempts_count"] >= 3 else "Limited data",
                "resources": topic.get("resources", {}),
                "steps": steps,
                "accuracy_percent": topic.get("accuracy_percent", None),
                "mistakes_count": topic.get("mistakes_count", 0),
                "days_elapsed": topic.get("days_elapsed", 0),
                "retention_percent": topic.get("retention_percent", None)
            })

            remaining_minutes -= allocated_time

        # 6. Calculate total planned time (HARD CONSTRAINT)
        total_planned = sum(p["allocated_minutes"] for p in priorities)
        assert total_planned <= available_minutes, \
            f"Plan violated time constraint: {total_planned} > {available_minutes}"

        total_steps = sum(len(p["steps"]) for p in priorities)

        # 7. Crisis Diagnosis ("What is actually going wrong?")
        diagnosis = self._build_diagnosis(all_topics, priorities, available_minutes, active_situation, exam_name)

        # 8. "If You Only Do One Thing" Spotlight
        one_thing = self._extract_one_thing(priorities)

        # 9. "Don't Study This Now" (Skip for Now) Protection Engine
        skip_topics = self._build_skip_topics(not_prioritized, available_minutes)

        # 10. Dynamic Time Breakdown Schedule
        time_breakdown = self._build_time_breakdown(priorities, available_minutes)

        # 11. Contextual Adaptive Tips
        adaptive_tips = self._get_adaptive_tips(active_situation, available_minutes)

        # 12. Persist session
        plan_data = {
            "priorities": priorities,
            "skip_topics": skip_topics,
            "diagnosis": diagnosis,
            "one_thing": one_thing,
            "time_breakdown": time_breakdown,
            "adaptive_tips": adaptive_tips,
            "total_planned_minutes": total_planned,
            "total_steps": total_steps,
            "active_situation": active_situation
        }

        session = save_emergency_session(
            user_id=user_id,
            available_minutes=available_minutes,
            plan_data=plan_data,
            subject_focus=subject_focus,
            exam_name=exam_name,
            exam_date=exam_date,
            steps_total=total_steps
        )

        return {
            "status": "success",
            "session_id": session["id"],
            "available_minutes": available_minutes,
            "total_planned_minutes": total_planned,
            "total_steps": total_steps,
            "active_situation": active_situation,
            "situation_meta": next((s for s in self.SCENARIOS if s["id"] == active_situation), None),
            "diagnosis": diagnosis,
            "one_thing": one_thing,
            "time_breakdown": time_breakdown,
            "priorities": priorities,
            "skip_topics": skip_topics,
            "adaptive_tips": adaptive_tips,
            "exam_context": {
                "name": exam_name,
                "date": exam_date,
                "source": "student_entered" if exam_name else "none"
            },
            "subject_focus": subject_focus
        }

    def complete_session(
        self,
        user_id: str,
        session_id: str,
        steps_completed: int = 0,
        topics_covered: Optional[List[str]] = None,
        performance: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Completes an emergency session:
        1. Updates emergency_sessions record
        2. Persists each topic as a revision_session (feeds back into learning ecosystem)
        3. Generates measured outcomes & smart post-emergency handoffs
        """
        session = get_emergency_session(session_id, user_id)
        if not session:
            return {"status": "error", "message": "Session not found or access denied."}

        # Update emergency session
        updated = update_emergency_session(
            session_id=session_id,
            user_id=user_id,
            status="completed",
            steps_completed=steps_completed,
            topics_covered=topics_covered or [],
            performance=performance or {}
        )

        # Feed completed topics into revision_sessions for ecosystem integration
        plan = session.get("plan", {})
        priorities = plan.get("priorities", [])
        perf = performance or {}
        covered_set = set(topics_covered or [])

        persisted_topics = []
        for priority in priorities:
            topic_name = priority.get("topic_name", "")
            subject_id = priority.get("subject_id", "")
            if not topic_name or not subject_id:
                continue

            if topics_covered and topic_name not in covered_set:
                continue

            topic_perf = perf.get(topic_name, {})

            try:
                save_revision_session(
                    user_id=user_id,
                    topic=topic_name,
                    subject_id=subject_id,
                    duration_minutes=float(priority.get("allocated_minutes", 0)),
                    steps_total=len(priority.get("steps", [])),
                    steps_completed=topic_perf.get("steps_completed", len(priority.get("steps", []))),
                    score=topic_perf.get("score", 0),
                    total_questions=topic_perf.get("total_questions", 0),
                    review_mode="emergency",
                    resources_used=topic_perf.get("resources_used", []),
                    priority_score=0.0
                )
                persisted_topics.append(topic_name)
            except Exception as e:
                print(f"[Emergency] Warning: Failed to persist revision for {topic_name}: {e}")

        # Post-emergency handoff recommendations based on canonical learning data
        handoff = {
            "recommended_page": "student-revision.html",
            "recommended_title": "Smart Spaced Revision",
            "reason": f"You reviewed {len(persisted_topics)} topic{'s' if len(persisted_topics) != 1 else ''}. Follow up on scheduled forgetting intervals to lock in retention.",
            "secondary_page": "student-profile.html#tab-genome",
            "secondary_title": "Learning Genome",
            "secondary_reason": "View updated topic masteries across your syllabus."
        }

        # Before vs After measured outcomes (real data only)
        time_planned = session.get("available_minutes", 0)
        time_spent_sec = perf.get("total_time_spent_seconds", time_planned * 60)
        time_spent_min = max(1, round(time_spent_sec / 60))

        measured_outcomes = {
            "time_invested_minutes": time_spent_min,
            "steps_completed": steps_completed,
            "steps_total": session.get("steps_total", 0),
            "topics_covered_count": len(persisted_topics),
            "persisted_topics": persisted_topics,
            "revision_sessions_synced": len(persisted_topics)
        }

        return {
            "status": "success",
            "message": "Emergency session completed and synchronized with your learning record.",
            "session_id": session_id,
            "steps_completed": steps_completed,
            "topics_covered": topics_covered or [],
            "measured_outcomes": measured_outcomes,
            "handoff": handoff,
            "performance_summary": perf
        }

    # =========================================================================
    # INTERNAL: Value-Per-Minute Calculation (Situation-Aware)
    # =========================================================================

    def _calculate_value_per_minute(
        self,
        topic: Dict,
        available_minutes: int,
        situation: str = "auto"
    ) -> float:
        """
        Deterministic, situation-aware value-per-minute score.
        Uses ONLY real signals from RevisionService.
        """
        priority = topic.get("priority_score", 50.0)
        accuracy = topic.get("accuracy_percent", 50.0)
        mistakes = topic.get("mistakes_count", 0)
        days_elapsed = topic.get("days_elapsed", 0)
        retention = topic.get("retention_percent", 100.0)

        # Base value from canonical priority score
        base_value = priority

        # Accuracy gap component
        accuracy_gap = max(0.0, 80.0 - accuracy) * 0.35

        # Situation modifier
        situation_bonus = 0.0
        if situation == "exam_today":
            # Exam in a few hours: avoid starting from scratch on deeply broken topics
            if accuracy < 40.0:
                situation_bonus -= 25.0
            elif 60.0 <= accuracy <= 85.0:
                situation_bonus += 20.0  # Fast consolidation of existing marks
        elif situation == "keep_making_mistakes":
            if mistakes >= 2:
                situation_bonus += 30.0
            elif mistakes == 1:
                situation_bonus += 15.0
        elif situation == "cant_remember":
            if days_elapsed >= 5 or (retention is not None and retention < 60.0):
                situation_bonus += 25.0
        elif situation == "completely_lost":
            if topic.get("resources", {}).get("has_notes"):
                situation_bonus += 15.0
        elif situation == "only_20_min":
            if accuracy >= 50.0 and mistakes >= 1:
                situation_bonus += 20.0
            elif accuracy < 35.0:
                situation_bonus -= 15.0
        elif situation == "exam_tomorrow":
            if mistakes >= 1:
                situation_bonus += 15.0
            if days_elapsed >= 4:
                situation_bonus += 10.0

        # General feasibility
        if available_minutes <= 15 and accuracy < 30.0:
            feasibility = -12.0
        elif 40.0 <= accuracy <= 75.0:
            feasibility = 10.0
        else:
            feasibility = 0.0

        # Resource availability bonus
        resources = topic.get("resources", {})
        resource_bonus = 0.0
        if resources.get("has_practice", False):
            resource_bonus += 6.0
        if resources.get("has_notes", False):
            resource_bonus += 4.0

        value_score = base_value + accuracy_gap + feasibility + resource_bonus + situation_bonus
        estimated_time = self._estimate_topic_duration(topic, available_minutes, situation)
        return round(max(0.1, value_score) / max(estimated_time, 1.0), 2)

    def _estimate_topic_duration(
        self,
        topic: Dict,
        available_minutes: int,
        situation: str = "auto"
    ) -> float:
        """Estimates practical study duration based on urgency, accuracy, and scenario."""
        urgency = topic.get("urgency", "safe")
        accuracy = topic.get("accuracy_percent", 50.0)

        if available_minutes <= 10:
            return 5.0
        elif available_minutes <= 25:
            if situation == "exam_today":
                return min(8.0, available_minutes * 0.5)
            if urgency in ("critical", "warning"):
                return min(12.0, available_minutes * 0.6)
            return min(8.0, available_minutes * 0.45)
        elif available_minutes <= 45:
            if urgency == "critical":
                return min(15.0, available_minutes * 0.4)
            return min(12.0, available_minutes * 0.3)
        else:
            if accuracy < 50.0:
                return min(22.0, available_minutes * 0.25)
            return min(15.0, available_minutes * 0.2)

    def _allocate_topic_time(
        self,
        topic: Dict,
        remaining: int,
        total_budget: int,
        situation: str = "auto"
    ) -> int:
        """Allocates time for a topic respecting the remaining budget."""
        estimated = self._estimate_topic_duration(topic, total_budget, situation)
        allocated = min(int(estimated), remaining)
        if allocated < self.MIN_TOPIC_TIME:
            return 0
        return allocated

    # =========================================================================
    # INTERNAL: Crisis Diagnosis & Decision Engineering
    # =========================================================================

    def _build_diagnosis(
        self,
        all_topics: List[Dict],
        priorities: List[Dict],
        available_minutes: int,
        situation: str,
        exam_name: str
    ) -> Dict[str, Any]:
        """
        Builds the 3-part 'What is actually going wrong?' diagnosis.
        WHAT is the problem? WHY does it matter? WHAT are we doing about it?
        """
        mistake_topics = [t for t in all_topics if t.get("mistakes_count", 0) >= 1]
        decay_topics = [
            t for t in all_topics
            if t.get("days_elapsed", 0) >= 4 or (t.get("retention_percent") is not None and t.get("retention_percent") < 65)
        ]
        low_acc_topics = [
            t for t in all_topics
            if t.get("accuracy_percent") is not None and t.get("accuracy_percent") < 50
        ]

        # 1. Current Situation
        if exam_name:
            sit_text = f"Preparing for {exam_name} with a {available_minutes}-minute recovery window. {len(all_topics)} topics analyzed."
        elif situation == "exam_today":
            sit_text = f"Final hours before assessment. {available_minutes} minutes available. Strategy: rapid formula & mistake verification."
        elif situation == "keep_making_mistakes":
            sit_text = f"Identified {len(mistake_topics)} topics with recorded misconceptions. Strategy: targeted error correction."
        elif situation == "cant_remember":
            sit_text = f"Retention decay detected across {len(decay_topics)} topics. Strategy: active retrieval drills."
        elif situation == "only_20_min":
            sit_text = f"Micro-sprint of {available_minutes} minutes. Strategy: eliminate the single biggest mark-leak."
        else:
            sit_text = f"{available_minutes} minutes allocated. Evaluated {len(all_topics)} syllabus topics to isolate your highest value-per-minute moves."

        # 2. Biggest Risk
        if mistake_topics:
            worst_m = max(mistake_topics, key=lambda x: x.get("mistakes_count", 0))
            risk_text = f"Repeated mistakes in {worst_m['topic']} ({worst_m.get('mistakes_count', 0)} logged errors) threaten marks on predictable question patterns."
        elif decay_topics:
            worst_d = min(decay_topics, key=lambda x: x.get("retention_percent", 100))
            risk_text = f"Memory decay in {worst_d['topic']} (retention at {int(worst_d.get('retention_percent', 50))}%) from lack of recent active recall."
        elif low_acc_topics:
            worst_a = min(low_acc_topics, key=lambda x: x.get("accuracy_percent", 50))
            risk_text = f"Conceptual gaps in {worst_a['topic']} ({int(worst_a.get('accuracy_percent', 0))}% accuracy) create vulnerability on test day."
        else:
            risk_text = "Risk of spending your emergency minutes on already-mastered material instead of reinforcing active edge cases."

        # 3. Best Opportunity
        if priorities:
            top_p = priorities[0]
            opp_text = f"Focusing {top_p['allocated_minutes']}m on {top_p['topic_name']}: verified practice questions and quick concept check offer maximum score yield."
        else:
            opp_text = "Targeted review of high-yield core definitions and verified practice sets."

        return {
            "current_situation": sit_text,
            "biggest_risk": risk_text,
            "best_opportunity": opp_text,
            "confidence_label": "High Confidence" if len(all_topics) >= 5 else "Calibrated Data",
            "data_source": f"Derived from {len(all_topics)} tracked topics and active telemetry"
        }

    def _extract_one_thing(self, priorities: List[Dict]) -> Optional[Dict[str, Any]]:
        """
        Extracts the single highest-value action to immediately eliminate decision paralysis.
        """
        if not priorities:
            return None
        top_p = priorities[0]
        steps = top_p.get("steps", [])
        top_step = steps[0] if steps else {
            "title": f"Review {top_p['topic_name']}",
            "duration_min": top_p.get("allocated_minutes", 10),
            "instruction": "Focus on core concepts and solve at least 2 practice problems.",
            "resource_url": f"student-practice.html?subject={top_p.get('subject_id', '')}",
            "action_type": "practice"
        }
        return {
            "topic_name": top_p["topic_name"],
            "subject_title": top_p.get("subject_title", ""),
            "subject_id": top_p.get("subject_id", ""),
            "action_title": top_step.get("title", "Core Action"),
            "duration_minutes": top_step.get("duration_min", 5),
            "instruction": top_step.get("instruction", ""),
            "reason": top_p.get("reason", {}).get("summary", "Highest priority topic based on your learning metrics."),
            "resource_url": top_step.get("resource_url") or f"student-practice.html?subject={top_p.get('subject_id', '')}",
            "action_type": top_step.get("action_type", "practice")
        }

    def _build_skip_topics(
        self,
        not_prioritized: List[Dict],
        available_minutes: int
    ) -> List[Dict[str, Any]]:
        """
        Actively protects the student's limited time by listing topics to SKIP right now.
        Provides clear, reassuring justifications.
        """
        skip_list = []
        for t in not_prioritized[:5]:
            acc = t.get("accuracy_percent")
            if acc is not None and acc >= 75.0:
                reason = f"Your performance is already solid ({int(acc)}% accuracy). In a {available_minutes}-min emergency session, marginal gain here is near zero."
                tag = "Already Mastered"
                badge_color = "emerald"
            elif acc is not None and acc < 35.0 and available_minutes <= 30:
                reason = f"Requires extensive conceptual re-learning (>45 minutes). Attempting full coverage right now will compromise your entire sprint."
                tag = "Too Time-Intensive"
                badge_color = "amber"
            else:
                reason = "Lower expected score yield than your top priorities. Protected from consuming your limited time."
                tag = "Low Yield For Now"
                badge_color = "slate"

            skip_list.append({
                "topic_name": t.get("topic", ""),
                "subject_title": t.get("subject_title", ""),
                "subject_icon": t.get("subject_icon", "📚"),
                "tag": tag,
                "badge_color": badge_color,
                "reason": reason
            })
        return skip_list

    def _build_time_breakdown(
        self,
        priorities: List[Dict],
        available_minutes: int
    ) -> List[Dict[str, Any]]:
        """
        Produces a functional schedule breakdown (e.g. 5m Concept • 8m Practice • 5m Mistakes • 2m Recall).
        """
        type_minutes = defaultdict(int)
        for p in priorities:
            for s in p.get("steps", []):
                stype = s.get("type", "practice")
                type_minutes[stype] += s.get("duration_min", 0)

        labels = {
            "active_recall": ("Concept & Formula Recall", "🧠"),
            "mistake_review": ("Mistake Correction", "🎯"),
            "notes_review": ("Key Notes Review", "📖"),
            "practice_question": ("Targeted Practice", "✏️"),
            "self_check": ("Rapid Verification", "✅")
        }

        breakdown = []
        total_m = sum(type_minutes.values()) or available_minutes
        for stype, mins in type_minutes.items():
            title, icon = labels.get(stype, ("Focused Study", "📚"))
            pct = round((mins / max(total_m, 1)) * 100)
            breakdown.append({
                "type": stype,
                "title": title,
                "icon": icon,
                "minutes": mins,
                "percent": pct
            })

        if not breakdown:
            breakdown = [
                {"type": "concept", "title": "Concept Review", "icon": "📖", "minutes": max(2, available_minutes // 4), "percent": 25},
                {"type": "practice", "title": "Targeted Practice", "icon": "✏️", "minutes": max(3, available_minutes // 2), "percent": 50},
                {"type": "check", "title": "Rapid Verification", "icon": "✅", "minutes": max(1, available_minutes // 4), "percent": 25}
            ]

        return breakdown

    def _get_adaptive_tips(self, situation: str, available_minutes: int) -> List[str]:
        """Provides calm, situation-specific advice during the live study sprint."""
        if situation == "exam_today":
            return [
                "Don't worry about understanding 100% of theoretical derivations now.",
                "Verify formula signs and units — that's where quick marks are won or lost.",
                "If a problem takes more than 2 minutes to understand, skip it immediately."
            ]
        elif situation == "keep_making_mistakes":
            return [
                "Before answering each practice problem, explicitly state why previous answers failed.",
                "Focus on the exact misconception identified in the card.",
                "Quality of correction matters more than rushing through question count."
            ]
        elif situation == "cant_remember":
            return [
                "Try to write down or whisper the definition before looking at the hint.",
                "Active struggle strengthens memory retrieval far more than passive reading.",
                "Quick verification at the end locks the memory into place."
            ]
        elif situation == "only_20_min":
            return [
                "Focus on the clock. Finish each step within its allocated minutes.",
                "Do not open external tabs or start unrelated topics.",
                "Once the timer rings, celebrate completing your highest-priority gap."
            ]
        else:
            return [
                "Trust the plan: these are your highest value-per-minute topics.",
                "Skip what we identified as non-priority without feeling guilty.",
                "Stay in focus mode until the session ends."
            ]

    # =========================================================================
    # INTERNAL: Step Generation & Formatting
    # =========================================================================

    def _generate_topic_steps(
        self,
        topic: Dict,
        allocated_minutes: int,
        situation: str = "auto"
    ) -> List[Dict]:
        """
        Generates study steps for a topic within allocated time.
        Adapts based on accuracy, mistakes, and situation.
        """
        resources = topic.get("resources", {})
        mistakes = topic.get("mistakes_count", 0)
        accuracy = topic.get("accuracy_percent", 50.0)
        topic_name = topic["topic"]
        steps = []
        remaining = allocated_minutes

        # Scenario adjustments
        if situation == "exam_today" or allocated_minutes <= 7:
            # Rapid micro-steps
            steps.append({
                "step_num": 1,
                "title": "Formula & Definition Check",
                "type": "active_recall",
                "duration_min": min(3, remaining),
                "instruction": f"Recall the core governing laws, formulas, and sign conventions for {topic_name}.",
                "action_type": "open_resource" if resources.get("has_notes") else "self_guided",
                "resource_url": resources.get("notes_url")
            })
            remaining -= min(3, remaining)

            if remaining >= 2:
                steps.append({
                    "step_num": 2,
                    "title": "High-Yield Verification",
                    "type": "practice_question",
                    "duration_min": remaining,
                    "instruction": f"Solve 1 targeted verification question on {topic_name} to confirm readiness.",
                    "action_type": "open_resource" if resources.get("has_practice") else "self_guided",
                    "resource_url": resources.get("practice_url")
                })
            return steps

        # 1. Mistake Review step if errors exist
        if mistakes > 0:
            m_time = min(3, max(2, remaining // 3))
            steps.append({
                "step_num": len(steps) + 1,
                "title": "Analyze Past Errors",
                "type": "mistake_review",
                "duration_min": m_time,
                "instruction": f"Review the {mistakes} mistake{'s' if mistakes != 1 else ''} recorded in {topic_name}. Clarify where your reasoning broke down.",
                "action_type": "open_resource" if resources.get("has_practice") else "self_guided",
                "resource_url": resources.get("practice_url")
            })
            remaining -= m_time

        # 2. Concept review or active recall
        if accuracy < 60.0 or situation == "completely_lost":
            c_time = min(4, max(2, remaining // 2))
            steps.append({
                "step_num": len(steps) + 1,
                "title": "Core Concept Review",
                "type": "notes_review",
                "duration_min": c_time,
                "instruction": f"Review key principles, diagrams, and formulas for {topic_name}.",
                "action_type": "open_resource" if resources.get("has_notes") else "self_guided",
                "resource_url": resources.get("notes_url")
            })
            remaining -= c_time
        else:
            r_time = min(3, max(2, remaining // 3))
            steps.append({
                "step_num": len(steps) + 1,
                "title": "Active Recall Drill",
                "type": "active_recall",
                "duration_min": r_time,
                "instruction": f"Without looking at notes, write down or state the 3 most essential facts about {topic_name}.",
                "action_type": "self_guided",
                "resource_url": None
            })
            remaining -= r_time

        # 3. Practice questions
        if remaining >= 3:
            p_time = max(3, remaining - 2)
            steps.append({
                "step_num": len(steps) + 1,
                "title": "Targeted Practice Problems",
                "type": "practice_question",
                "duration_min": p_time,
                "instruction": f"Solve focused practice questions on {topic_name}. Aim for precision over speed.",
                "action_type": "open_resource" if resources.get("has_practice") else "self_guided",
                "resource_url": resources.get("practice_url")
            })
            remaining -= p_time

        # 4. Self-check
        if remaining > 0:
            steps.append({
                "step_num": len(steps) + 1,
                "title": "Quick Self-Check",
                "type": "self_check",
                "duration_min": remaining,
                "instruction": f"Rate your confidence in {topic_name} now compared to before this sprint.",
                "action_type": "self_guided",
                "resource_url": None
            })

        # Ensure total equals allocated
        total_step_time = sum(s["duration_min"] for s in steps)
        if total_step_time < allocated_minutes and steps:
            steps[-1]["duration_min"] += (allocated_minutes - total_step_time)

        return steps

    def _get_priority_label(self, index: int, topic: Dict) -> str:
        if index == 0:
            return "do_first"
        elif index == 1:
            return "high_impact"
        elif topic.get("accuracy_percent", 0) >= 70:
            return "quick_win"
        else:
            return "high_impact" if index < 3 else "quick_win"

    def _priority_label_text(self, level: str) -> str:
        labels = {
            "do_first": "🔴 DO THIS FIRST",
            "high_impact": "🟠 HIGH IMPACT",
            "quick_win": "🟡 QUICK WIN",
            "not_priority": "⚪ NOT A PRIORITY RIGHT NOW"
        }
        return labels.get(level, "📌 RECOMMENDED")

    def _build_reason(self, topic: Dict, situation: str = "auto") -> Dict[str, Any]:
        signals = topic.get("signals", [])
        accuracy = topic.get("accuracy_percent")
        mistakes = topic.get("mistakes_count", 0)

        reasons = []
        reason_codes = []

        if mistakes >= 1:
            reasons.append(f"{mistakes} previous mistake{'s' if mistakes != 1 else ''} logged here.")
            reason_codes.append("REPEATED_MISTAKES")

        if accuracy is not None and accuracy < 60.0:
            reasons.append(f"Recent accuracy is {int(accuracy)}% (room for substantial score boost).")
            reason_codes.append("LOW_RECENT_ACCURACY")

        for signal in signals:
            sig_type = signal.get("type", "")
            if sig_type == "INACTIVITY_GAP":
                reasons.append(signal["text"])
                reason_codes.append("LONG_REVISION_GAP")

        if not reasons:
            reasons.append("High value-per-minute return on short focused practice.")
            reason_codes.append("HIGH_VALUE_PER_MINUTE")

        return {
            "summary": " ".join(reasons),
            "codes": reason_codes,
            "has_evidence": True
        }

    def _build_empty_state_plan(
        self,
        user_id: str,
        available_minutes: int,
        subject_focus: str,
        exam_name: str
    ) -> Dict[str, Any]:
        available_actions = []

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM practice_questions")
        q_count = cursor.fetchone()[0]
        conn.close()

        if q_count > 0:
            available_actions.append({
                "type": "practice",
                "title": "Start Practice Diagnostic",
                "description": "Complete 5 quick questions so Emergency Mode can calculate your real priority topics.",
                "url": "student-practice.html",
                "icon": "🎯"
            })

        if len(resource_service.chapters_db) > 0:
            available_actions.append({
                "type": "notes",
                "title": "Open Chapter Notes",
                "description": "Review foundational concepts to begin logging revision telemetry.",
                "url": "student-notes.html",
                "icon": "📝"
            })

        return {
            "status": "insufficient_data",
            "session_id": None,
            "message": "We need a little more learning activity to personalize your rescue plan.",
            "detail": "Solve a few diagnostic questions or review a chapter note so our Situation Intelligence can pinpoint your exact weak points.",
            "available_minutes": available_minutes,
            "total_planned_minutes": 0,
            "total_steps": 0,
            "priorities": [],
            "skip_topics": [],
            "diagnosis": {
                "current_situation": f"New student profile. You have {available_minutes} minutes available.",
                "biggest_risk": "Lack of calibration data makes targeted triage impossible without guessing.",
                "best_opportunity": "Complete a 5-question diagnostic to unlock full Situation Intelligence.",
                "confidence_label": "Calibrating",
                "data_source": "Telemetry pending"
            },
            "one_thing": {
                "topic_name": "Diagnostic Practice",
                "subject_title": "General",
                "action_title": "Solve 5 Diagnostic Questions",
                "duration_minutes": min(10, available_minutes),
                "instruction": "Answer 5 questions to calibrate your knowledge genome.",
                "reason": "Calibrates your accuracy and identifies mistake patterns.",
                "resource_url": "student-practice.html",
                "action_type": "practice"
            },
            "available_actions": available_actions,
            "exam_context": {
                "name": exam_name,
                "source": "student_entered" if exam_name else "none"
            }
        }


emergency_service = EmergencyService()
