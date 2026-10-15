"""
VIDYA – Quiz Center page
Built-in sample quizzes + AI-generated quizzes when API is available.
Results are stored persistently.
"""

import streamlit as st
import sys, os, json

_APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _APP_DIR not in sys.path:
    sys.path.insert(0, _APP_DIR)

from modules import quiz_engine, ai_assistant as ai, database as db


def render():
    st.markdown(
        '<h2 style="font-weight:800;margin-bottom:0.3rem;">🧠 Quiz Center</h2>'
        '<p style="color:#6b7280;margin-bottom:1.5rem;">'
        'Test your knowledge with sample or AI-generated quizzes.</p>',
        unsafe_allow_html=True
    )

    # ── Quiz configuration ─────────────────────────────────────────────────────
    st.markdown("### Configure Your Quiz")
    cfg1, cfg2, cfg3 = st.columns(3)
    with cfg1:
        subjects = quiz_engine.get_subjects()
        subject = st.selectbox("Subject", subjects)
    with cfg2:
        topics = quiz_engine.get_topics(subject)
        topic = st.selectbox("Topic", topics if topics else ["General"])
    with cfg3:
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

    quiz_type = st.radio(
        "Quiz source",
        ["📚 Sample Quiz (works offline)", "🤖 AI-Generated Quiz (requires API key)"],
        horizontal=True
    )

    if st.button("🚀 Start Quiz", use_container_width=True):
        questions = None

        if "Sample" in quiz_type:
            questions = quiz_engine.get_sample_quiz(subject, topic)
            if not questions:
                st.warning(f"No sample quiz available for {subject} – {topic}. Try a different topic.")
                return
            st.session_state.quiz_source = "sample"
        else:
            if not ai.is_available():
                st.error("⚠️ AI service not configured. Use the Sample Quiz option or configure your API key in Settings.")
                return
            with st.spinner("Generating quiz with AI…"):
                context = st.session_state.get("extracted_pdf_text", "")
                json_str = ai.generate_quiz_json(f"{subject} – {topic} ({difficulty})", context)
                questions = quiz_engine.parse_ai_quiz(json_str)
            if not questions:
                st.error("AI returned an unexpected format. Please try again.")
                return
            st.session_state.quiz_source = "ai"

        st.session_state.quiz_questions = questions
        st.session_state.quiz_answers = {}
        st.session_state.quiz_subject = subject
        st.session_state.quiz_topic = topic
        st.session_state.quiz_difficulty = difficulty
        st.session_state.quiz_submitted = False
        st.rerun()

    # ── Active quiz ────────────────────────────────────────────────────────────
    if "quiz_questions" in st.session_state and not st.session_state.get("quiz_submitted", False):
        questions = st.session_state.quiz_questions
        source_label = (
            "📚 Sample Quiz (demonstration data)"
            if st.session_state.get("quiz_source") == "sample"
            else "🤖 AI-Generated Quiz"
        )
        st.markdown(f"---\n### {source_label}")
        st.caption(
            f"Subject: {st.session_state.quiz_subject} · "
            f"Topic: {st.session_state.quiz_topic} · "
            f"Difficulty: {st.session_state.quiz_difficulty}"
        )

        for i, q in enumerate(questions):
            st.markdown(f"**Q{i+1}. {q['question']}**")
            options = q.get("options", [])
            answer = st.radio(
                f"Select your answer for Q{i+1}",
                options,
                key=f"quiz_q_{i}",
                index=None,
                label_visibility="collapsed"
            )
            st.session_state.quiz_answers[i] = answer

        if st.button("✅ Submit Quiz", use_container_width=True):
            unanswered = [i for i, a in st.session_state.quiz_answers.items() if a is None]
            if unanswered:
                st.warning(f"Please answer all questions before submitting. Unanswered: Q{', Q'.join(str(u+1) for u in unanswered)}")
            else:
                st.session_state.quiz_submitted = True
                st.rerun()

    # ── Results ────────────────────────────────────────────────────────────────
    if st.session_state.get("quiz_submitted"):
        questions = st.session_state.quiz_questions
        answers = st.session_state.quiz_answers
        score = 0

        st.markdown("---\n### 📊 Quiz Results")

        for i, q in enumerate(questions):
            user_ans = answers.get(i)
            correct_ans = q.get("answer")
            is_correct = str(user_ans).strip() == str(correct_ans).strip()
            if is_correct:
                score += 1
                st.success(f"**Q{i+1}. {q['question']}**\n\n✅ Your answer: {user_ans} — Correct!")
            else:
                st.error(
                    f"**Q{i+1}. {q['question']}**\n\n"
                    f"❌ Your answer: {user_ans}\n\n"
                    f"✅ Correct answer: {correct_ans}"
                )
            exp = q.get("explanation")
            if exp:
                with st.expander("💡 Explanation"):
                    st.markdown(exp)

        max_score = len(questions)
        pct = round(score / max_score * 100) if max_score else 0

        st.markdown(f"---\n## 🏆 Score: {score} / {max_score} ({pct}%)")
        if pct >= 80:
            st.balloons()
            st.success("Excellent work! 🎉")
        elif pct >= 60:
            st.info("Good effort! Review the topics you missed.")
        else:
            st.warning("Keep practising! Check the AI Tutor for help with difficult topics.")

        # Persist result
        db.save_quiz_result(
            st.session_state.quiz_subject,
            st.session_state.quiz_topic,
            st.session_state.quiz_difficulty,
            score,
            max_score,
        )

        if st.button("🔄 Take Another Quiz", use_container_width=True):
            for key in ["quiz_questions", "quiz_answers", "quiz_submitted", "quiz_source",
                        "quiz_subject", "quiz_topic", "quiz_difficulty"]:
                st.session_state.pop(key, None)
            st.rerun()

    # ── Previous results ───────────────────────────────────────────────────────
    st.markdown("---\n### 📋 Previous Quiz Results")
    results = db.get_quiz_results(limit=10)
    if results:
        for r in results:
            pct = round(r["score"] / r["max_score"] * 100) if r["max_score"] else 0
            col_a, col_b, col_c, col_d = st.columns([2, 2, 1, 1])
            with col_a:
                st.markdown(f"**{r['subject']}** – {r['topic']}")
            with col_b:
                st.markdown(f"*{r['difficulty']}* · {r['taken_at'][:10]}")
            with col_c:
                st.markdown(f"{r['score']} / {r['max_score']}")
            with col_d:
                colour = "#16a34a" if pct >= 80 else ("#ca8a04" if pct >= 60 else "#dc2626")
                st.markdown(
                    f'<span style="color:{colour};font-weight:700;">{pct}%</span>',
                    unsafe_allow_html=True
                )
            st.divider()
    else:
        st.info("No quiz attempts yet. Take your first quiz above!")
