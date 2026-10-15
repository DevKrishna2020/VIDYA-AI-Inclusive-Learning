"""
VIDYA – progress_tracker.py
Rule-based recommendation engine built on top of stored progress data.
"""

from __future__ import annotations
from datetime import date, timedelta
from . import database as db


def get_stats() -> dict:
    """Return an aggregated summary of the student's learning progress."""
    lessons = db.get_lessons()
    quiz_results = db.get_quiz_results(limit=50)

    total_lessons = len(lessons)
    completed_lessons = sum(1 for l in lessons if l["completed"])
    completion_pct = round((completed_lessons / total_lessons * 100) if total_lessons else 0)

    avg_score = 0.0
    if quiz_results:
        percentages = [
            (r["score"] / r["max_score"] * 100) for r in quiz_results if r["max_score"] > 0
        ]
        avg_score = round(sum(percentages) / len(percentages), 1) if percentages else 0.0

    weekly = db.get_weekly_study_minutes()
    total_minutes_this_week = sum(weekly.values())

    return {
        "total_lessons": total_lessons,
        "completed_lessons": completed_lessons,
        "completion_pct": completion_pct,
        "total_quizzes": len(quiz_results),
        "avg_quiz_score": avg_score,
        "weekly_minutes": total_minutes_this_week,
        "weekly_hours": round(total_minutes_this_week / 60, 1),
    }


def get_recommendations() -> dict[str, list[str]]:
    """
    Rule-based recommendation engine.

    Returns a dict with:
      'suggested'  – lessons to start next
      'revision'   – lessons/topics needing revisiting (low quiz score)
    """
    lessons = db.get_lessons()
    quiz_results = db.get_quiz_results(limit=50)

    # Identify subjects with low quiz performance (< 60 %)
    weak_subjects: set[str] = set()
    for r in quiz_results:
        if r["max_score"] > 0 and (r["score"] / r["max_score"]) < 0.6:
            weak_subjects.add(r["subject"])

    # Suggest next incomplete lessons
    suggested = [
        f"{l['subject']} – {l['title']}"
        for l in lessons if not l["completed"]
    ][:3]

    # Revision: incomplete lessons in weak subjects
    revision = [
        f"{l['subject']} – {l['title']}"
        for l in lessons
        if not l["completed"] and l["subject"] in weak_subjects
    ][:3]

    if not revision and weak_subjects:
        revision = [f"Review: {s}" for s in list(weak_subjects)[:3]]

    return {"suggested": suggested, "revision": revision}


def get_weekly_plan() -> list[dict[str, str]]:
    """Return a simple 5-day study plan based on incomplete lessons."""
    lessons = db.get_lessons()
    incomplete = [l for l in lessons if not l["completed"]]

    plan = []
    today = date.today()
    for i, lesson in enumerate(incomplete[:5]):
        study_day = today + timedelta(days=i)
        plan.append({
            "day": study_day.strftime("%A"),
            "subject": lesson["subject"],
            "task": lesson["title"],
        })
    return plan
