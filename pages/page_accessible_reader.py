"""
VIDYA – Accessible Reader page
Upload PDFs, extract text, simplify, translate, and listen.
"""

import streamlit as st
import sys, os

_APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _APP_DIR not in sys.path:
    sys.path.insert(0, _APP_DIR)

from modules import pdf_reader, ai_assistant as ai, translation, speech


def render():
    st.markdown(
        '<h2 style="font-weight:800;margin-bottom:0.3rem;">📄 Accessible Reader</h2>'
        '<p style="color:#6b7280;margin-bottom:1.5rem;">'
        'Upload a PDF to read, simplify, translate, and listen to educational content.</p>',
        unsafe_allow_html=True
    )

    # ── Tabs ───────────────────────────────────────────────────────────────────
    default_tab = st.session_state.pop("reader_tab", "read")
    tab_labels = ["📖 Read", "✏️ Simplify", "🌐 Translate", "🔊 Listen"]
    tab_map = {"read": 0, "simplify": 1, "translate": 2, "speech": 3}
    default_idx = tab_map.get(default_tab, 0)

    tabs = st.tabs(tab_labels)
    active_tab_idx = default_idx  # Streamlit doesn't support programmatic tab selection directly

    # ── Upload ─────────────────────────────────────────────────────────────────
    st.markdown("---")
    uploaded = st.file_uploader(
        "Upload a PDF document",
        type=["pdf"],
        help="Text-based PDFs only. Scanned image PDFs are not supported."
    )

    if uploaded:
        file_bytes = uploaded.read()
        with st.spinner("Extracting text…"):
            try:
                text = pdf_reader.extract_text(file_bytes)
                pages = pdf_reader.page_count(file_bytes)
                st.session_state.extracted_pdf_text = text
                st.session_state.pdf_filename = uploaded.name
                st.success(f"✅ Extracted text from **{uploaded.name}** ({pages} pages, {len(text):,} characters)")
            except pdf_reader.PDFExtractionError as exc:
                st.error(f"❌ {exc}")
                st.session_state.extracted_pdf_text = ""
                st.session_state.pdf_filename = ""
    elif "extracted_pdf_text" not in st.session_state:
        st.session_state.extracted_pdf_text = ""
        st.session_state.pdf_filename = ""

    pdf_text = st.session_state.get("extracted_pdf_text", "")

    # ── Tab: Read ──────────────────────────────────────────────────────────────
    with tabs[0]:
        st.markdown("### Extracted Text")
        if pdf_text:
            st.text_area("Document content", pdf_text, height=400, label_visibility="collapsed")
        else:
            st.info("Upload a PDF above to read its content here.", icon="📄")

    # ── Tab: Simplify ──────────────────────────────────────────────────────────
    with tabs[1]:
        st.markdown("### Simplify Text")

        # Allow manual input even without a PDF
        simplify_source = st.radio(
            "Text source",
            ["Use uploaded PDF", "Enter text manually"],
            horizontal=True,
            key="simplify_source"
        )
        if simplify_source == "Enter text manually":
            input_text = st.text_area("Paste text to simplify", height=200, key="manual_simplify_input")
        else:
            input_text = pdf_text

        if st.button("✏️ Simplify Text", key="btn_simplify", use_container_width=True):
            if not input_text:
                st.warning("No text to simplify. Upload a PDF or enter text manually.")
            elif not ai.is_available():
                st.error("⚠️ AI service not configured. See Settings page for setup instructions.")
            else:
                with st.spinner("Simplifying…"):
                    simplified = ai.simplify_text(input_text[:4000])
                st.session_state.simplified_text = simplified

        if "simplified_text" in st.session_state:
            st.markdown("**Simplified Version:**")
            st.text_area("", st.session_state.simplified_text, height=300, label_visibility="collapsed")
            st.download_button(
                "⬇️ Download Simplified Text",
                data=st.session_state.simplified_text,
                file_name="simplified_text.txt",
                mime="text/plain"
            )

    # ── Tab: Translate ─────────────────────────────────────────────────────────
    with tabs[2]:
        st.markdown("### Translate Text")

        translate_source = st.radio(
            "Text source",
            ["Use uploaded PDF", "Enter text manually"],
            horizontal=True,
            key="translate_source"
        )
        if translate_source == "Enter text manually":
            translate_input = st.text_area("Paste text to translate", height=200, key="manual_translate_input")
        else:
            translate_input = pdf_text

        target_lang = st.selectbox(
            "Translate to",
            list(translation.SUPPORTED_LANGUAGES.keys()),
            index=0
        )

        if not translation.is_available():
            st.info(
                "Translation uses deep-translator (free, no API key needed). "
                "Install it with: `pip install deep-translator`",
                icon="ℹ️"
            )

        if st.button("🌐 Translate", key="btn_translate", use_container_width=True):
            if not translate_input:
                st.warning("No text to translate.")
            else:
                with st.spinner(f"Translating to {target_lang}…"):
                    result = translation.translate(translate_input[:4500], target_lang)
                st.session_state.translated_text = result
                st.session_state.translated_lang = target_lang

        if "translated_text" in st.session_state:
            st.markdown(f"**Translation ({st.session_state.get('translated_lang', '')}):**")
            st.text_area("", st.session_state.translated_text, height=300, label_visibility="collapsed")
            st.download_button(
                "⬇️ Download Translation",
                data=st.session_state.translated_text,
                file_name="translation.txt",
                mime="text/plain"
            )

    # ── Tab: Listen ────────────────────────────────────────────────────────────
    with tabs[3]:
        st.markdown("### Read Aloud (Text-to-Speech)")

        if not speech.is_available():
            st.warning(
                "gTTS is not installed. Run `pip install gTTS` to enable text-to-speech.",
                icon="🔊"
            )

        speech_source = st.radio(
            "Read which text?",
            ["Extracted PDF text", "Simplified text", "Translated text", "Enter manually"],
            key="speech_source"
        )
        speech_lang = st.selectbox(
            "Language",
            list(speech.SUPPORTED_LANGUAGES.keys()),
            key="speech_lang"
        )

        if speech_source == "Extracted PDF text":
            tts_text = pdf_text
        elif speech_source == "Simplified text":
            tts_text = st.session_state.get("simplified_text", "")
        elif speech_source == "Translated text":
            tts_text = st.session_state.get("translated_text", "")
        else:
            tts_text = st.text_area("Enter text to read aloud", height=200, key="manual_tts")

        if st.button("🔊 Generate Audio", use_container_width=True):
            if not tts_text:
                st.warning("No text selected. Please upload a PDF or enter text manually.")
            elif not speech.is_available():
                st.error("gTTS is not installed.")
            else:
                with st.spinner("Generating audio…"):
                    audio_bytes = speech.text_to_speech(tts_text[:9000], speech_lang)
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3")
                    st.download_button(
                        "⬇️ Download Audio",
                        data=audio_bytes,
                        file_name="vidya_audio.mp3",
                        mime="audio/mp3"
                    )
                else:
                    st.error("Audio generation failed. The text may be too short or contain unsupported characters.")

    # ── Summary download (always available if text extracted) ──────────────────
    if pdf_text:
        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("📝 Generate Summary (AI)", use_container_width=True, key="btn_summary"):
                if not ai.is_available():
                    st.error("⚠️ AI service not configured.")
                else:
                    with st.spinner("Generating summary…"):
                        summary = ai.ask(
                            f"Please provide a concise summary of the following document:\n\n{pdf_text[:5000]}",
                            mode="general"
                        )
                    st.session_state.pdf_summary = summary

        if "pdf_summary" in st.session_state:
            st.markdown("**Document Summary:**")
            st.text_area("", st.session_state.pdf_summary, height=200, label_visibility="collapsed")
            with col_b:
                st.download_button(
                    "⬇️ Download Summary",
                    data=st.session_state.pdf_summary,
                    file_name="summary.txt",
                    mime="text/plain",
                    key="dl_summary"
                )
