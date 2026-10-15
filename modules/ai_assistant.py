"""
VIDYA – ai_assistant.py
Wrapper around the OpenAI-compatible chat completion API.
API key is read from the OPENAI_API_KEY environment variable or from
the Streamlit secrets file — never hardcoded.
"""

from __future__ import annotations
import os
import textwrap

_CLIENT = None
_API_AVAILABLE: bool | None = None  # None = not yet checked


def _get_client():
    """Lazily initialise the OpenAI client."""
    global _CLIENT, _API_AVAILABLE

    # Always resolve the key fresh so a key entered in the sidebar takes effect
    # without a page reload.
    api_key = os.getenv("OPENAI_API_KEY", "")

    # Check Streamlit session_state (key entered via the sidebar input)
    if not api_key:
        try:
            import streamlit as st
            api_key = st.session_state.get("openai_api_key", "").strip()
        except Exception:
            pass

    # Also check Streamlit secrets (available at runtime, not import time)
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("OPENAI_API_KEY", "")
        except Exception:
            pass

    if not api_key:
        _API_AVAILABLE = False
        _CLIENT = None
        return None

    try:
        from openai import OpenAI
        _CLIENT = OpenAI(api_key=api_key)
        _API_AVAILABLE = True
        return _CLIENT
    except ImportError:
        _API_AVAILABLE = False
        _CLIENT = None
        return None


def is_available() -> bool:
    """Return True if the AI service is configured and reachable."""
    return _get_client() is not None


def ask(
    question: str,
    context: str = "",
    mode: str = "general",
    model: str = "gpt-4o-mini",
) -> str:
    """
    Send a question to the LLM and return the answer as a string.

    Parameters
    ----------
    question : str
        The student's question.
    context : str
        Optional text from an uploaded PDF to ground the answer.
    mode : str
        'general' | 'document' | 'simplify' | 'quiz'
    model : str
        OpenAI model identifier.
    """
    client = _get_client()
    if client is None:
        return (
            "⚠️ AI service is not configured. "
            "Please add your OPENAI_API_KEY to the environment or Streamlit secrets. "
            "See the Settings page for instructions."
        )

    system_parts = [
        "You are VIDYA, a friendly and encouraging AI learning assistant. "
        "Your goal is to help students understand academic topics clearly. "
        "Provide accurate, age-appropriate, and curriculum-aligned explanations.",
    ]

    if mode == "document" and context:
        system_parts.append(
            "The student has uploaded a document. Use the following extracted text "
            "as your primary context. Clearly indicate when your answer comes from "
            "the document versus your general knowledge.\n\n"
            f"DOCUMENT CONTENT:\n{context[:6000]}"
        )
    elif mode == "simplify":
        system_parts.append(
            "Rewrite the provided text using simpler language suitable for a "
            "secondary school student. Keep all key information but remove jargon."
        )
    elif mode == "quiz":
        system_parts.append(
            "Generate exactly 5 multiple-choice questions in JSON. "
            "Format: [{\"question\":\"...\",\"options\":[\"A\",\"B\",\"C\",\"D\"],"
            "\"answer\":\"A\",\"explanation\":\"...\"}]. "
            "Return only valid JSON, no extra text."
        )

    system_prompt = "\n\n".join(system_parts)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": question},
            ],
            max_tokens=1024,
            temperature=0.4,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        return f"⚠️ AI request failed: {exc}"


def simplify_text(text: str) -> str:
    """Return a simplified version of the supplied text."""
    return ask(text, mode="simplify")


def generate_quiz_json(topic: str, context: str = "") -> str:
    """Return a JSON string containing 5 quiz questions."""
    prompt = f"Generate a quiz about: {topic}"
    return ask(prompt, context=context, mode="quiz")
