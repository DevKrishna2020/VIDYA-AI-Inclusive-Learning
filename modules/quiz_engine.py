"""
VIDYA – quiz_engine.py
Built-in sample quiz bank and AI-powered quiz generation.
"""

from __future__ import annotations
import json

# ── Sample quiz bank (works without AI) ───────────────────────────────────────

SAMPLE_QUIZZES: dict[str, dict[str, list[dict]]] = {
    "Science": {
        "Physics": [
            {
                "question": "What is Newton's First Law of Motion?",
                "options": [
                    "An object stays at rest or in uniform motion unless acted upon by a net external force.",
                    "Force equals mass times acceleration.",
                    "For every action there is an equal and opposite reaction.",
                    "Energy cannot be created or destroyed.",
                ],
                "answer": "An object stays at rest or in uniform motion unless acted upon by a net external force.",
                "explanation": "Newton's First Law is also known as the Law of Inertia.",
            },
            {
                "question": "Which unit measures electrical resistance?",
                "options": ["Volt", "Ampere", "Ohm", "Watt"],
                "answer": "Ohm",
                "explanation": "Resistance is measured in Ohms (Ω), named after Georg Simon Ohm.",
            },
            {
                "question": "What is the speed of light in a vacuum (approx.)?",
                "options": ["3 × 10⁸ m/s", "3 × 10⁶ m/s", "3 × 10¹⁰ m/s", "3 × 10⁴ m/s"],
                "answer": "3 × 10⁸ m/s",
                "explanation": "The speed of light in a vacuum is approximately 299,792,458 m/s ≈ 3 × 10⁸ m/s.",
            },
        ],
        "Biology": [
            {
                "question": "What organelle is known as the powerhouse of the cell?",
                "options": ["Nucleus", "Mitochondria", "Ribosome", "Golgi apparatus"],
                "answer": "Mitochondria",
                "explanation": "Mitochondria produce ATP through cellular respiration, supplying energy to the cell.",
            },
            {
                "question": "What is the basic unit of heredity?",
                "options": ["Cell", "Chromosome", "Gene", "Protein"],
                "answer": "Gene",
                "explanation": "Genes are segments of DNA that encode instructions for building proteins.",
            },
        ],
    },
    "Mathematics": {
        "Algebra": [
            {
                "question": "Solve for x: 2x + 4 = 12",
                "options": ["x = 2", "x = 4", "x = 6", "x = 8"],
                "answer": "x = 4",
                "explanation": "2x = 12 − 4 = 8, so x = 4.",
            },
            {
                "question": "What is the quadratic formula?",
                "options": [
                    "x = (−b ± √(b²−4ac)) / 2a",
                    "x = (b ± √(b²+4ac)) / 2a",
                    "x = (−b ± √(b²−4ac)) / a",
                    "x = (b ± √(b²−4ac)) / 2a",
                ],
                "answer": "x = (−b ± √(b²−4ac)) / 2a",
                "explanation": "The quadratic formula solves ax² + bx + c = 0 for x.",
            },
        ],
        "Geometry": [
            {
                "question": "What is the sum of interior angles in a triangle?",
                "options": ["90°", "180°", "270°", "360°"],
                "answer": "180°",
                "explanation": "The interior angles of any triangle always add up to 180°.",
            },
        ],
    },
    "Computer Science": {
        "Python Basics": [
            {
                "question": "Which keyword is used to define a function in Python?",
                "options": ["func", "define", "def", "function"],
                "answer": "def",
                "explanation": "In Python, `def` is followed by the function name and parameters.",
            },
            {
                "question": "What does `len([1, 2, 3])` return?",
                "options": ["2", "3", "4", "1"],
                "answer": "3",
                "explanation": "The list has three elements, so len() returns 3.",
            },
        ],
    },
}


def get_sample_quiz(subject: str, topic: str) -> list[dict] | None:
    """Return sample questions for the given subject/topic, or None if not found."""
    return SAMPLE_QUIZZES.get(subject, {}).get(topic)


def get_subjects() -> list[str]:
    return list(SAMPLE_QUIZZES.keys())


def get_topics(subject: str) -> list[str]:
    return list(SAMPLE_QUIZZES.get(subject, {}).keys())


def parse_ai_quiz(json_str: str) -> list[dict] | None:
    """
    Parse a JSON string returned by the AI into a list of question dicts.
    Returns None if parsing fails.
    """
    try:
        # Strip markdown code fences if present
        cleaned = json_str.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            cleaned = "\n".join(lines[1:-1])
        return json.loads(cleaned)
    except Exception:
        return None
