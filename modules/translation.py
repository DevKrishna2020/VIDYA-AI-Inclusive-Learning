"""
VIDYA – translation.py
Text translation using the deep-translator library (free, no API key needed).
Falls back gracefully if the library is not installed.
"""

from __future__ import annotations

SUPPORTED_LANGUAGES = {
    "English":    "en",
    "Hindi":      "hi",
    "Spanish":    "es",
    "French":     "fr",
    "Arabic":     "ar",
    "Swahili":    "sw",
    "Portuguese": "pt",
    "German":     "de",
    "Chinese (Simplified)": "zh-CN",
    "Japanese":   "ja",
}

try:
    from deep_translator import GoogleTranslator as _GT
    _TRANSLATOR_AVAILABLE = True
except ImportError:
    _TRANSLATOR_AVAILABLE = False


def is_available() -> bool:
    return _TRANSLATOR_AVAILABLE


def translate(text: str, target_language: str) -> str:
    """
    Translate *text* into *target_language* (a key in SUPPORTED_LANGUAGES).
    Returns the translated string, or an informative error message.
    """
    if not _TRANSLATOR_AVAILABLE:
        return (
            "Translation is not available. "
            "Install deep-translator: `pip install deep-translator`"
        )

    lang_code = SUPPORTED_LANGUAGES.get(target_language)
    if not lang_code:
        return f"Unsupported language: {target_language}"

    if lang_code == "en":
        return text  # Already English

    # deep-translator has a 5000-character limit per call; chunk if needed
    max_chunk = 4500
    if len(text) <= max_chunk:
        try:
            return _GT(source="auto", target=lang_code).translate(text)
        except Exception as exc:
            return f"Translation failed: {exc}"

    # Chunk the text
    parts = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]
    translated_parts = []
    for part in parts:
        try:
            translated_parts.append(_GT(source="auto", target=lang_code).translate(part))
        except Exception as exc:
            return f"Translation failed: {exc}"
    return " ".join(translated_parts)
