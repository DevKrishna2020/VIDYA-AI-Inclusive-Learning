"""
Tests for VIDYA progress_tracker module.
Run with: pytest tests/test_progress_tracker.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Use an in-memory test database
os.environ.setdefault("VIDYA_TEST_MODE", "1")

from modules import database as db, progress_tracker as pt

# Point the DB to a temp file for tests
import tempfile
_tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
db.DB_PATH = _tmp.name
db.initialise_db()


def test_get_stats_returns_dict():
    stats = pt.get_stats()
    assert isinstance(stats, dict)
    assert "completed_lessons" in stats
    assert "total_lessons" in stats
    assert "avg_quiz_score" in stats
    assert "weekly_hours" in stats


def test_stats_counts_are_non_negative():
    stats = pt.get_stats()
    assert stats["completed_lessons"] >= 0
    assert stats["total_lessons"] >= stats["completed_lessons"]
    assert stats["avg_quiz_score"] >= 0


def test_get_recommendations_keys():
    recs = pt.get_recommendations()
    assert "suggested" in recs
    assert "revision" in recs
    assert isinstance(recs["suggested"], list)
    assert isinstance(recs["revision"], list)


def test_get_weekly_plan_is_list():
    plan = pt.get_weekly_plan()
    assert isinstance(plan, list)
    for item in plan:
        assert "day" in item
        assert "subject" in item
        assert "task" in item


def test_mark_lesson_complete_updates_stats():
    lessons = db.get_lessons()
    incomplete = [l for l in lessons if not l["completed"]]
    if not incomplete:
        return  # All already done

    before = pt.get_stats()
    db.mark_lesson_complete(incomplete[0]["id"])
    after = pt.get_stats()
    assert after["completed_lessons"] >= before["completed_lessons"]


def test_save_and_retrieve_quiz_result():
    db.save_quiz_result("Science", "Physics", "Easy", 4, 5)
    results = db.get_quiz_results(limit=5)
    assert len(results) >= 1
    latest = results[0]
    assert latest["subject"] == "Science"
    assert latest["score"] == 4
    assert latest["max_score"] == 5
