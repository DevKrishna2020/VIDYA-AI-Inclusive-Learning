"""
VIDYA – Progress page
Interactive Plotly charts showing study analytics.
"""

import streamlit as st
import sys, os
from datetime import date, timedelta

_APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _APP_DIR not in sys.path:
    sys.path.insert(0, _APP_DIR)

from modules import database as db, progress_tracker as pt

try:
    import plotly.graph_objects as go
    import plotly.express as px
    _PLOTLY = True
except ImportError:
    _PLOTLY = False


def render():
    st.markdown(
        '<h2 style="font-weight:800;margin-bottom:0.3rem;">📊 Progress Analytics</h2>'
        '<p style="color:#6b7280;margin-bottom:1.5rem;">'
        'Visualise your learning journey over time.</p>',
        unsafe_allow_html=True
    )

    if not _PLOTLY:
        st.error("Plotly is not installed. Run `pip install plotly` to enable charts.")
        return

    stats = pt.get_stats()

    # ── Summary metrics ────────────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Lessons Completed", f"{stats['completed_lessons']} / {stats['total_lessons']}")
    m2.metric("Completion", f"{stats['completion_pct']}%")
    m3.metric("Quizzes Taken", stats["total_quizzes"])
    m4.metric("Avg Quiz Score", f"{stats['avg_quiz_score']}%")

    st.markdown("---")

    row1_left, row1_right = st.columns(2)

    # ── Chart 1: Subject-wise completion ──────────────────────────────────────
    with row1_left:
        st.markdown("#### Subject-wise Lesson Completion")
        lessons = db.get_lessons()
        subjects = list(dict.fromkeys(l["subject"] for l in lessons))
        completed_counts = [sum(1 for l in lessons if l["subject"] == s and l["completed"]) for s in subjects]
        total_counts = [sum(1 for l in lessons if l["subject"] == s) for s in subjects]
        pcts = [round(c/t*100) if t else 0 for c, t in zip(completed_counts, total_counts)]

        colours = ["#7c6fcd", "#a78bfa", "#6ee7b7", "#fcd34d"]
        fig1 = go.Figure(go.Bar(
            x=subjects,
            y=pcts,
            marker_color=colours[:len(subjects)],
            text=[f"{p}%" for p in pcts],
            textposition="outside",
        ))
        fig1.update_layout(
            yaxis_title="Completion %",
            yaxis_range=[0, 110],
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=10, b=10),
            height=300,
        )
        st.plotly_chart(fig1, use_container_width=True)

    # ── Chart 2: Quiz score history ────────────────────────────────────────────
    with row1_right:
        st.markdown("#### Quiz Score History")
        results = db.get_quiz_results(limit=15)
        if results:
            labels = [f"Q{i+1}" for i in range(len(results))]
            scores = [round(r["score"] / r["max_score"] * 100) if r["max_score"] else 0 for r in reversed(results)]
            subjects_r = [r["subject"] for r in reversed(results)]

            fig2 = go.Figure(go.Scatter(
                x=labels,
                y=scores,
                mode="lines+markers",
                line=dict(color="#7c6fcd", width=2.5),
                marker=dict(size=8, color="#7c6fcd"),
                hovertext=subjects_r,
            ))
            fig2.add_hline(y=60, line_dash="dash", line_color="#ef4444", annotation_text="Pass threshold (60%)")
            fig2.update_layout(
                yaxis_title="Score %",
                yaxis_range=[0, 105],
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10, b=10),
                height=300,
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No quiz results yet. Take quizzes in the Quiz Center!")

    st.markdown("---")

    row2_left, row2_right = st.columns(2)

    # ── Chart 3: Weekly study activity ─────────────────────────────────────────
    with row2_left:
        st.markdown("#### Weekly Study Activity (minutes)")
        weekly = db.get_weekly_study_minutes()
        # Fill in missing days
        today = date.today()
        all_days = [(today - timedelta(days=6 - i)).isoformat() for i in range(7)]
        day_labels = [(today - timedelta(days=6 - i)).strftime("%a") for i in range(7)]
        minutes = [weekly.get(d, 0) for d in all_days]

        if any(minutes):
            fig3 = go.Figure(go.Bar(
                x=day_labels,
                y=minutes,
                marker_color="#6ee7b7",
                text=minutes,
                textposition="outside",
            ))
            fig3.update_layout(
                yaxis_title="Minutes",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10, b=10),
                height=300,
            )
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info(
                "No study sessions recorded this week. "
                "Complete lessons in **My Learning** to log study time."
            )

    # ── Chart 4: Completion doughnut ───────────────────────────────────────────
    with row2_right:
        st.markdown("#### Overall Learning Goals")
        lessons = db.get_lessons()
        completed = sum(1 for l in lessons if l["completed"])
        remaining = len(lessons) - completed

        fig4 = go.Figure(go.Pie(
            labels=["Completed", "Remaining"],
            values=[completed, remaining],
            hole=0.55,
            marker_colors=["#7c6fcd", "#e5e7eb"],
            textinfo="label+percent",
        ))
        fig4.update_layout(
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=10, b=10),
            height=300,
        )
        st.plotly_chart(fig4, use_container_width=True)

    # ── Recommendations ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 💡 Personalised Recommendations")
    recs = pt.get_recommendations()
    col_s, col_r = st.columns(2)
    with col_s:
        st.markdown("**Suggested next lessons:**")
        if recs["suggested"]:
            for t in recs["suggested"]:
                st.markdown(f"📌 {t}")
        else:
            st.success("All lessons complete!")
    with col_r:
        st.markdown("**Topics needing revision:**")
        if recs["revision"]:
            for t in recs["revision"]:
                st.markdown(f"🔁 {t}")
        else:
            st.success("No weak topics identified yet.")

    # ── Weekly plan ─────────────────────────────────────────────────────────────
    st.markdown("---\n#### 📅 Your Weekly Study Plan")
    plan = pt.get_weekly_plan()
    if plan:
        plan_cols = st.columns(len(plan))
        for col, item in zip(plan_cols, plan):
            with col:
                st.markdown(
                    f'<div class="vidya-card" style="text-align:center;">'
                    f'<div style="font-weight:700;color:#7c6fcd;">{item["day"]}</div>'
                    f'<div style="font-size:0.78rem;font-weight:600;margin-top:0.3rem;">{item["subject"]}</div>'
                    f'<div style="font-size:0.75rem;color:#6b7280;margin-top:0.2rem;">{item["task"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
    else:
        st.success("All lessons are complete — review past material or add new subjects!")
