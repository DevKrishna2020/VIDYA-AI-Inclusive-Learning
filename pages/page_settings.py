"""
VIDYA – Settings page
Font size, contrast, TTS controls, language, and AI API key setup.
"""

import streamlit as st
import sys, os

_APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _APP_DIR not in sys.path:
    sys.path.insert(0, _APP_DIR)

from modules import database as db
from modules import ai_assistant as ai, speech


def render():
    st.markdown(
        '<h2 style="font-weight:800;margin-bottom:0.3rem;">⚙️ Settings</h2>'
        '<p style="color:#6b7280;margin-bottom:1.5rem;">'
        'Personalise your learning experience and configure services.</p>',
        unsafe_allow_html=True
    )

    tab_a, tab_b, tab_c = st.tabs(["♿ Accessibility", "🔊 Text-to-Speech", "🔑 API & Services"])

    # ── Accessibility settings ─────────────────────────────────────────────────
    with tab_a:
        st.markdown("### Display & Reading")

        current_font = int(db.get_setting("font_size", "15"))
        font_size = st.slider(
            "Font size (px)",
            min_value=12,
            max_value=24,
            value=current_font,
            step=1,
            help="Adjusts the base font size across the application."
        )

        current_hc = db.get_setting("high_contrast", "false") == "true"
        high_contrast = st.toggle(
            "High-contrast mode",
            value=current_hc,
            help="Dark background with bright text for better contrast."
        )

        current_layout = db.get_setting("comfortable_layout", "false") == "true"
        comfortable = st.toggle(
            "Comfortable reading layout",
            value=current_layout,
            help="Increases line spacing and limits content width."
        )

        current_anim = db.get_setting("reduce_animations", "false") == "true"
        reduce_anim = st.toggle(
            "Reduce animations",
            value=current_anim,
            help="Hides transitions and loading animations."
        )

        st.markdown("### Language Preference")
        from modules.translation import SUPPORTED_LANGUAGES
        current_lang = db.get_setting("ui_language", "English")
        lang_list = list(SUPPORTED_LANGUAGES.keys())
        lang_idx = lang_list.index(current_lang) if current_lang in lang_list else 0
        ui_language = st.selectbox("Interface language", lang_list, index=lang_idx)

        if st.button("💾 Save Accessibility Settings", use_container_width=True):
            db.set_setting("font_size", str(font_size))
            db.set_setting("high_contrast", "true" if high_contrast else "false")
            db.set_setting("comfortable_layout", "true" if comfortable else "false")
            db.set_setting("reduce_animations", "true" if reduce_anim else "false")
            db.set_setting("ui_language", ui_language)

            # Apply to session state for immediate effect
            st.session_state.font_size = font_size
            st.session_state.high_contrast = high_contrast
            st.session_state.ui_language = ui_language

            st.success("✅ Accessibility settings saved. Reload the page to apply all changes.")

        st.markdown("---")
        st.markdown("### Accessibility Compliance Notes")
        st.markdown("""
        VIDYA is designed to meet the following accessibility principles:

        - ✅ **Color contrast** — text meets WCAG AA contrast ratios
        - ✅ **Text labels** — all form controls have visible labels
        - ✅ **Keyboard navigation** — Streamlit controls are keyboard-accessible
        - ✅ **Error messages** — all errors include plain-language descriptions
        - ✅ **No color-only communication** — status is conveyed with icons and text
        - ✅ **Scalable text** — font size is user-adjustable
        """)

    # ── TTS settings ───────────────────────────────────────────────────────────
    with tab_b:
        st.markdown("### Text-to-Speech Controls")

        if speech.is_available():
            st.success("✅ gTTS is installed and ready.", icon="🔊")
        else:
            st.error(
                "gTTS is not installed. Run the following command in your terminal:\n\n"
                "```\npip install gTTS\n```\n\n"
                "Then restart the application.",
                icon="❌"
            )

        current_tts_lang = db.get_setting("tts_language", "English")
        tts_lang_list = list(speech.SUPPORTED_LANGUAGES.keys())
        tts_idx = tts_lang_list.index(current_tts_lang) if current_tts_lang in tts_lang_list else 0
        tts_language = st.selectbox("Default TTS language", tts_lang_list, index=tts_idx)

        if st.button("💾 Save TTS Settings", use_container_width=True, key="save_tts"):
            db.set_setting("tts_language", tts_language)
            st.success("✅ TTS settings saved.")

        st.markdown("---")
        st.markdown("### Test Text-to-Speech")
        test_text = st.text_area(
            "Enter text to test",
            value="Hello! Welcome to VIDYA, your inclusive learning platform.",
            height=100,
            key="tts_test_text"
        )
        test_lang = st.selectbox("Language for test", tts_lang_list, key="tts_test_lang")
        if st.button("▶️ Play Test Audio", use_container_width=True):
            if not speech.is_available():
                st.error("Install gTTS first.")
            else:
                with st.spinner("Generating…"):
                    audio = speech.text_to_speech(test_text, test_lang)
                if audio:
                    st.audio(audio, format="audio/mp3")
                else:
                    st.error("Audio generation failed.")

    # ── API & services ─────────────────────────────────────────────────────────
    with tab_c:
        st.markdown("### AI Service Configuration")

        if ai.is_available():
            st.success("✅ AI service (OpenAI) is configured and connected.", icon="🤖")
        else:
            st.warning("⚠️ AI service is not configured. Features requiring AI will show setup messages.", icon="⚠️")

        st.markdown("""
        VIDYA uses the **OpenAI API** for AI-powered features. Your API key is **never stored in source code**.

        #### Option 1: Environment variable (recommended for local use)

        Set the variable before launching the app:

        **Windows (PowerShell):**
        ```powershell
        $env:OPENAI_API_KEY = "sk-..."
        streamlit run app.py
        ```

        **macOS / Linux:**
        ```bash
        export OPENAI_API_KEY="sk-..."
        streamlit run app.py
        ```

        #### Option 2: Streamlit secrets file (recommended for Streamlit Cloud)

        Create `.streamlit/secrets.toml` in the project root:

        ```toml
        OPENAI_API_KEY = "sk-..."
        ```

        This file is listed in `.gitignore` and will not be committed to version control.

        #### Getting an API key

        1. Visit [platform.openai.com](https://platform.openai.com)
        2. Create an account and navigate to **API keys**
        3. Click **Create new secret key**
        4. Copy the key and set it using one of the methods above

        ⚠️ Never share your API key publicly or commit it to a repository.
        """)

        st.markdown("---")
        st.markdown("### Installed Package Status")

        checks = {
            "streamlit":       "Core framework",
            "pypdf":           "PDF text extraction",
            "plotly":          "Progress charts",
            "openai":          "AI assistant",
            "gTTS":            "Text-to-speech",
            "deep_translator": "Text translation",
            "pandas":          "Data handling",
        }

        for pkg, desc in checks.items():
            try:
                __import__(pkg)
                st.markdown(f"✅ **{pkg}** — {desc}")
            except ImportError:
                st.markdown(f"❌ **{pkg}** — {desc} *(not installed)*")
