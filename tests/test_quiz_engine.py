"""
Tests for VIDYA quiz_engine module.
Run with: pytest tests/test_quiz_engine.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from modules.quiz_engine import (
    get_subjects,
    get_topics,
    get_sample_quiz,
    parse_ai_quiz,
)


def test_get_subjects_returns_list():
    subjects = get_subjects()
    assert isinstance(subjects, list)
    assert len(subjects) > 0


def test_get_topics_returns_list_for_valid_subject():
    subjects = get_subjects()
    topics = get_topics(subjects[0])
    assert isinstance(topics, list)
    assert len(topics) > 0


def test_get_topics_returns_empty_for_unknown_subject():
    assert get_topics("Nonexistent Subject") == []


def test_get_sample_quiz_valid():
    questions = get_sample_quiz("Science", "Physics")
    assert questions is not None
    assert len(questions) > 0
    q = questions[0]
    assert "question" in q
    assert "options" in q
    assert "answer" in q
    assert "explanation" in q


def test_get_sample_quiz_missing_topic():
    assert get_sample_quiz("Science", "QuantumAstronomy") is None


def test_parse_ai_quiz_valid_json():
    sample = '[{"question":"What is 2+2?","options":["3","4","5","6"],"answer":"4","explanation":"Basic addition."}]'
    result = parse_ai_quiz(sample)
    assert result is not None
    assert len(result) == 1
    assert result[0]["answer"] == "4"


def test_parse_ai_quiz_with_code_fence():
    fenced = '```json\n[{"question":"Test?","options":["A","B"],"answer":"A","explanation":"Test."}]\n```'
    result = parse_ai_quiz(fenced)
    assert result is not None


def test_parse_ai_quiz_invalid_json():
    assert parse_ai_quiz("not json at all {{{{") is None
