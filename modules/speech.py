"""
VIDYA – speech.py
Text-to-speech using the gTTS (Google Text-to-Speech) library.
Returns raw MP3 bytes that can be played with st.audio().
"""

from __future__ import annotations
import io

try:
    from gtts import gTTS as _gTTS
    _GTTS_AVAILABLE = True
except ImportError:
    _GTTS_AVAILABLE = False

SUPPORTED_LANGUAGES = {
    "English":    "en",
    "Hindi":      "hi",
    "Spanish":    "es",
    "French":     "fr",
    "Arabic":     "ar",
    "Portuguese": "pt",
    "German":     "de",
    "Chinese (Simplified)": "zh-CN",
    "Japanese":   "ja",
}


def is_available() -> bool:
    return _GTTS_AVAILABLE


def text_to_speech(text: str, language: str = "English") -> bytes | None:
    """
    Convert *text* to MP3 audio bytes.

    Returns
    -------
    bytes
        Raw MP3 data ready for st.audio().
    None
        If gTTS is not installed or an error occurs.
    """
    if not _GTTS_AVAILABLE:
        return None

    lang_code = SUPPORTED_LANGUAGES.get(language, "en")

    # gTTS recommends <= 10 000 characters per call
    text = text[:9000]

    try:
        tts = _gTTS(text=text, lang=lang_code, slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf.read()
    except Exception:
        return None
