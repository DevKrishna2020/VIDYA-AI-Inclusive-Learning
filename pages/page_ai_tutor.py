"""
VIDYA – AI Tutor page
Chat interface backed by OpenAI API (or graceful fallback).
Supports general questions and document-specific questions.
"""

import streamlit as st
import sys, os

_APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _APP_DIR not in sys.path:
    sys.path.insert(0, _APP_DIR)

from modules import ai_assistant as ai


def render():
    st.markdown(
        '<h2 style="font-weight:800;margin-bottom:0.3rem;">🤖 AI Tutor</h2>'
        '<p style="color:#6b7280;margin-bottom:1.5rem;">'
        'Ask questions, request explanations, or discuss your uploaded documents.</p>',
        unsafe_allow_html=True
    )

    # API status banner
    if ai.is_available():
        st.success("✅ AI service is connected and ready.", icon="🤖")
    else:
        st.warning(
            "⚠️ AI service is not configured. "
            "Add your OPENAI_API_KEY to the environment or Streamlit secrets. "
            "See the **Settings** page for instructions. "
            "All other features remain fully functional.",
            icon="⚠️"
        )

    # Mode selector
    mode = st.radio(
        "Question mode",
        ["General Question", "Document-Based Question"],
        horizontal=True,
    )

    # PDF context (shared from Accessible Reader via session state)
    pdf_text = st.session_state.get("extracted_pdf_text", "")

    if mode == "Document-Based Question":
        if pdf_text:
            st.info(
                f"📄 Using document uploaded in Accessible Reader "
                f"({len(pdf_text):,} characters of extracted text).",
                icon="📄"
            )
        else:
            st.warning(
                "No document loaded. Please upload a PDF in the **Accessible Reader** first.",
                icon="📄"
            )

    # Chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Prompt helper buttons
    st.markdown("**Quick prompts:**")
    qp1, qp2, qp3, qp4 = st.columns(4)
    preset = ""
    with qp1:
        if st.button("Explain simply", use_container_width=True):
            preset = "Please explain this topic simply with a real-world example: "
    with qp2:
        if st.button("Step-by-step", use_container_width=True):
            preset = "Give me a step-by-step explanation of: "
    with qp3:
        if st.button("Give an example", use_container_width=True):
            preset = "Give me a practical example of: "
    with qp4:
        if st.button("Summarise", use_container_width=True):
            preset = "Summarise the key points about: "

    # Chat input
    user_input = st.chat_input("Ask your question here…")

    if user_input or preset:
        question = (preset + user_input) if (user_input and preset) else (user_input or preset)

        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                if mode == "Document-Based Question" and pdf_text:
                    answer = ai.ask(question, context=pdf_text, mode="document")
                else:
                    answer = ai.ask(question, mode="general")
            st.markdown(answer)

        st.session_state.chat_history.append({"role": "assistant", "content": answer})

    if st.session_state.chat_history:
        if st.button("🗑️ Clear conversation"):
            st.session_state.chat_history = []
            st.rerun()
