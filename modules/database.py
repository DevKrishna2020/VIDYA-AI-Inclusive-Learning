"""
VIDYA – database.py
SQLite-backed persistence for learning progress, quiz results, and settings.
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vidya_data.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def initialise_db() -> None:
    """Create all required tables if they do not already exist."""
    conn = get_connection()
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS lessons (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            subject     TEXT    NOT NULL,
            title       TEXT    NOT NULL,
            description TEXT,
            completed   INTEGER NOT NULL DEFAULT 0,
            completed_at TEXT
        );

        CREATE TABLE IF NOT EXISTS quiz_results (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            subject     TEXT    NOT NULL,
            topic       TEXT    NOT NULL,
            difficulty  TEXT    NOT NULL,
            score       INTEGER NOT NULL,
            max_score   INTEGER NOT NULL,
            taken_at    TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS study_sessions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            subject     TEXT    NOT NULL,
            duration_minutes INTEGER NOT NULL DEFAULT 0,
            session_date TEXT   NOT NULL
        );

        CREATE TABLE IF NOT EXISTS settings (
            key   TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
    """)

    # Seed sample lesson catalogue if empty
    cur.execute("SELECT COUNT(*) FROM lessons")
    if cur.fetchone()[0] == 0:
        sample_lessons = [
            ("Science",           "Introduction to Physics",      "Basics of motion and forces",          0, None),
            ("Science",           "Cell Biology",                 "Structure and function of cells",       0, None),
            ("Mathematics",       "Algebra Fundamentals",         "Variables, equations, and functions",   0, None),
            ("Mathematics",       "Geometry Essentials",          "Shapes, angles, and theorems",          1, "2024-11-10"),
            ("Computer Science",  "Python Basics",                "Variables, loops, and functions",       1, "2024-11-12"),
            ("Computer Science",  "Data Structures",              "Lists, dicts, stacks, and queues",      0, None),
            ("Languages",         "English Grammar",              "Tenses, voice, and clauses",            1, "2024-11-15"),
            ("Languages",         "Academic Writing",             "Essays, reports, and citations",        0, None),
        ]
        cur.executemany(
            "INSERT INTO lessons (subject, title, description, completed, completed_at) VALUES (?,?,?,?,?)",
            sample_lessons
        )

    conn.commit()
    conn.close()


# ── Lessons ────────────────────────────────────────────────────────────────────

def get_lessons(subject: str | None = None) -> list[dict]:
    conn = get_connection()
    if subject:
        rows = conn.execute(
            "SELECT * FROM lessons WHERE subject=? ORDER BY id", (subject,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM lessons ORDER BY subject, id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mark_lesson_complete(lesson_id: int) -> None:
    conn = get_connection()
    conn.execute(
        "UPDATE lessons SET completed=1, completed_at=? WHERE id=?",
        (datetime.now().isoformat(timespec="seconds"), lesson_id)
    )
    conn.commit()
    conn.close()


# ── Quiz results ───────────────────────────────────────────────────────────────

def save_quiz_result(subject: str, topic: str, difficulty: str, score: int, max_score: int) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO quiz_results (subject, topic, difficulty, score, max_score, taken_at) VALUES (?,?,?,?,?,?)",
        (subject, topic, difficulty, score, max_score, datetime.now().isoformat(timespec="seconds"))
    )
    conn.commit()
    conn.close()


def get_quiz_results(limit: int = 20) -> list[dict]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM quiz_results ORDER BY taken_at DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── Study sessions ─────────────────────────────────────────────────────────────

def log_study_session(subject: str, duration_minutes: int) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO study_sessions (subject, duration_minutes, session_date) VALUES (?,?,?)",
        (subject, duration_minutes, datetime.now().date().isoformat())
    )
    conn.commit()
    conn.close()


def get_weekly_study_minutes() -> dict[str, int]:
    """Returns a dict of {date_str: total_minutes} for the last 7 days."""
    conn = get_connection()
    rows = conn.execute(
        """SELECT session_date, SUM(duration_minutes) as total
           FROM study_sessions
           WHERE session_date >= date('now','-6 days')
           GROUP BY session_date
           ORDER BY session_date"""
    ).fetchall()
    conn.close()
    return {r["session_date"]: r["total"] for r in rows}


# ── Settings ───────────────────────────────────────────────────────────────────

def get_setting(key: str, default: str = "") -> str:
    conn = get_connection()
    row = conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    conn.close()
    return row["value"] if row else default


def set_setting(key: str, value: str) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO settings (key, value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, value)
    )
    conn.commit()
    conn.close()
