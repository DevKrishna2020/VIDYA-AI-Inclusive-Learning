"""
VIDYA – My Learning page
Displays lesson catalogue grouped by subject.
Students can mark lessons as complete and track their progress.
"""

import streamlit as st
import sys, os

# Ensure modules are importable
_APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _APP_DIR not in sys.path:
    sys.path.insert(0, _APP_DIR)

from modules import database as db


def render():
    st.markdown(
        '<h2 style="font-weight:800;margin-bottom:0.3rem;">📖 My Learning</h2>'
        '<p style="color:#6b7280;margin-bottom:1.5rem;">Browse your lesson catalogue and track your progress.</p>',
        unsafe_allow_html=True
    )

    lessons = db.get_lessons()

    subjects = list(dict.fromkeys(l["subject"] for l in lessons))
    default_idx = 0
    if "selected_subject" in st.session_state and st.session_state.selected_subject in subjects:
        default_idx = subjects.index(st.session_state.selected_subject)

    selected_subject = st.selectbox("Filter by subject", ["All Subjects"] + subjects, index=default_idx + 1 if default_idx else 0)

    if selected_subject != "All Subjects":
        filtered = [l for l in lessons if l["subject"] == selected_subject]
    else:
        filtered = lessons

    badge_map = {
        "Science":          ("badge-science",  "🔬"),
        "Mathematics":      ("badge-math",     "📐"),
        "Computer Science": ("badge-cs",       "💻"),
        "Languages":        ("badge-lang",     "🗣️"),
    }

    col1, col2 = st.columns(2)
    for i, lesson in enumerate(filtered):
        col = col1 if i % 2 == 0 else col2
        badge_cls, icon = badge_map.get(lesson["subject"], ("badge-cs", "📌"))
        status_icon = "✅" if lesson["completed"] else "⬜"
        status_label = "Completed" if lesson["completed"] else "Not started"

        with col:
            with st.container():
                st.markdown(
                    f'<div class="vidya-card">'
                    f'<div style="display:flex;justify-content:space-between;align-items:flex-start;">'
                    f'<div>'
                    f'<span class="vidya-badge {badge_cls}">{icon} {lesson["subject"]}</span>'
                    f'<h4 style="margin:0.5rem 0 0.2rem 0;font-size:0.97rem;">{lesson["title"]}</h4>'
                    f'<p style="margin:0;font-size:0.82rem;color:#6b7280;">{lesson["description"]}</p>'
                    f'</div>'
                    f'<span style="font-size:1.3rem;">{status_icon}</span>'
                    f'</div>'
                    f'<div style="margin-top:0.7rem;font-size:0.78rem;color:#9ca3af;">'
                    f'Status: {status_label}'
                    + (f' · Completed {lesson["completed_at"][:10]}' if lesson["completed_at"] else '')
                    + f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                if not lesson["completed"]:
                    if st.button(
                        f"✔ Mark as Complete",
                        key=f"complete_{lesson['id']}",
                        use_container_width=True,
                    ):
                        db.mark_lesson_complete(lesson["id"])
                        db.log_study_session(lesson["subject"], 30)
                        st.success(f"Marked '{lesson['title']}' as complete!")
                        st.rerun()
                else:
                    st.markdown(
                        '<p style="color:#16a34a;font-size:0.85rem;font-weight:600;margin-top:0.4rem;">✅ Lesson complete</p>',
                        unsafe_allow_html=True
                    )

    # Overall progress summary
    st.markdown("---")
    st.markdown('<p class="vidya-section-title">Overall Completion</p>', unsafe_allow_html=True)
    total = len(lessons)
    completed = sum(1 for l in lessons if l["completed"])
    pct = int(completed / total * 100) if total else 0
    st.progress(pct / 100)
    st.caption(f"{completed} of {total} lessons completed ({pct}%)")
