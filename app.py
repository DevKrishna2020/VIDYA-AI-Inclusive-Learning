"""
VIDYA — AI-Powered Inclusive Learning and Educational Accessibility Platform
Main entry point (Dashboard page)
"""

import streamlit as st
import os
import sys

# ── Path setup ─────────────────────────────────────────────────────────────────
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from modules import database as db
from modules import progress_tracker as pt

# ── Page configuration ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VIDYA – Inclusive Learning",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Initialise DB ──────────────────────────────────────────────────────────────
db.initialise_db()

# ── Global CSS ─────────────────────────────────────────────────────────────────
def inject_css() -> None:
    font_size = st.session_state.get("font_size", 15)
    high_contrast = st.session_state.get("high_contrast", False)

    bg_color      = "#1a1a2e" if high_contrast else "#f2f0ff"
    surface_color = "#16213e" if high_contrast else "#ffffff"
    text_color    = "#ffffff" if high_contrast else "#2d2d3a"
    muted_color   = "#a0aec0" if high_contrast else "#6b7280"
    border_color  = "#4a5568" if high_contrast else "#e5e7eb"
    sidebar_bg    = "#1a1a2e" if high_contrast else "#2d2b55"
    accent        = "#7c6fcd"

    st.markdown(f"""
    <style>
    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, 'Segoe UI', system-ui, sans-serif;
        font-size: {font_size}px;
        color: {text_color};
    }}

    /* ── App background ── */
    .stApp {{
        background-color: {bg_color};
        background-image:
            radial-gradient(ellipse at 10% 20%, rgba(124,111,205,0.08) 0%, transparent 60%),
            radial-gradient(ellipse at 90% 80%, rgba(163,209,232,0.07) 0%, transparent 60%);
    }}

    /* ── Main content area ── */
    .block-container {{
        background: {surface_color};
        border-radius: 20px;
        padding: 2rem 2.5rem 3rem 2.5rem !important;
        margin-top: 1rem;
        border: 1px solid {border_color};
        max-width: 1200px;
    }}

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {{
        background: {sidebar_bg} !important;
        border-right: 1px solid rgba(255,255,255,0.08);
    }}
    [data-testid="stSidebar"] * {{
        color: #e2e8f0 !important;
    }}
    [data-testid="stSidebar"] .stRadio > label {{
        font-weight: 600;
        font-size: 0.8rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #a0aec0 !important;
        padding-bottom: 0.4rem;
    }}
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {{
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 0.5rem 0.8rem;
        margin-bottom: 2px;
        transition: background 0.2s;
        font-weight: 500;
    }}
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {{
        background: rgba(124,111,205,0.3);
    }}

    /* ── Metric cards ── */
    [data-testid="stMetric"] {{
        background: {bg_color};
        border-radius: 14px;
        padding: 1rem 1.2rem;
        border: 1px solid {border_color};
    }}
    [data-testid="stMetric"] label {{
        color: {muted_color} !important;
        font-size: 0.78rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    [data-testid="stMetric"] [data-testid="stMetricValue"] {{
        font-size: 1.8rem;
        font-weight: 700;
        color: {text_color} !important;
    }}

    /* ── Buttons ── */
    .stButton > button {{
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s;
        border: none;
    }}
    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(124,111,205,0.25);
    }}

    /* ── Progress bar ── */
    .stProgress > div > div > div > div {{
        background: linear-gradient(90deg, {accent}, #a78bfa);
        border-radius: 99px;
    }}
    .stProgress > div > div > div {{
        border-radius: 99px;
        background: {border_color};
    }}

    /* ── Text inputs and text areas ── */
    .stTextInput input, .stTextArea textarea {{
        border-radius: 10px;
        border: 1px solid {border_color};
        background: {bg_color};
        color: {text_color};
    }}

    /* ── Selectbox ── */
    .stSelectbox select {{
        border-radius: 10px;
        border: 1px solid {border_color};
    }}

    /* ── Expander ── */
    .streamlit-expanderHeader {{
        border-radius: 10px;
        font-weight: 600;
    }}

    /* ── Tab bar ── */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 10px 10px 0 0;
        padding: 0.5rem 1.2rem;
    }}

    /* ── Divider ── */
    hr {{
        border: none;
        border-top: 1px solid {border_color};
        margin: 1.5rem 0;
    }}

    /* ── Utility card ── */
    .vidya-card {{
        background: {bg_color};
        border: 1px solid {border_color};
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
    }}

    /* ── Section header ── */
    .vidya-section-title {{
        font-size: 1.1rem;
        font-weight: 700;
        color: {text_color};
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}

    /* ── Badge ── */
    .vidya-badge {{
        display: inline-block;
        padding: 2px 10px;
        border-radius: 99px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.04em;
    }}
    .badge-science  {{ background: #dbeafe; color: #1d4ed8; }}
    .badge-math     {{ background: #fef9c3; color: #854d0e; }}
    .badge-cs       {{ background: #dcfce7; color: #166534; }}
    .badge-lang     {{ background: #fce7f3; color: #9d174d; }}

    /* ── Hide default Streamlit elements ── */
    #MainMenu, footer {{ visibility: hidden; }}
    header[data-testid="stHeader"] {{ background: transparent; }}
    </style>
    """, unsafe_allow_html=True)

inject_css()

# ── Sidebar navigation ─────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        # Brand name (no logo)
        st.markdown(
            '<div style="padding:0.5rem 0 1.5rem 0;">'
            '<span style="font-size:1.5rem;font-weight:800;color:#e2e8f0;">VIDYA</span>'
            '<br><span style="font-size:0.72rem;color:#a0aec0;letter-spacing:0.06em;">INCLUSIVE LEARNING</span>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown("---")

        nav_items = {
            "🏠  Dashboard":         "Dashboard",
            "📖  My Learning":       "My Learning",
            "🤖  AI Tutor":          "AI Tutor",
            "📄  Accessible Reader": "Accessible Reader",
            "🧠  Quiz Center":       "Quiz Center",
            "📊  Progress":          "Progress",
            "⚙️  Settings":          "Settings",
        }

        if "current_page" not in st.session_state:
            st.session_state.current_page = "Dashboard"

        for label, page in nav_items.items():
            selected = st.session_state.current_page == page
            btn_style = (
                "background:rgba(124,111,205,0.35);border-radius:10px;padding:0.5rem 0.8rem;"
                "color:#fff;font-weight:600;width:100%;text-align:left;border:none;cursor:pointer;"
                "margin-bottom:2px;font-size:0.93rem;"
            ) if selected else (
                "background:transparent;border-radius:10px;padding:0.5rem 0.8rem;"
                "color:#cbd5e1;font-weight:500;width:100%;text-align:left;border:none;cursor:pointer;"
                "margin-bottom:2px;font-size:0.93rem;"
            )
            if st.button(label, key=f"nav_{page}", use_container_width=True):
                st.session_state.current_page = page
                st.rerun()

        st.markdown("---")

        # ── API Key input ──────────────────────────────────────────────────────
        st.markdown(
            '<p style="font-size:0.72rem;font-weight:600;color:#a0aec0;'
            'letter-spacing:0.06em;text-transform:uppercase;margin-bottom:0.3rem;">'
            '🔑 OpenAI API Key</p>',
            unsafe_allow_html=True,
        )
        api_key_input = st.text_input(
            label="OpenAI API Key",
            value=st.session_state.get("openai_api_key", ""),
            type="password",
            placeholder="sk-…",
            label_visibility="collapsed",
            key="sidebar_api_key_input",
        )
        if api_key_input != st.session_state.get("openai_api_key", ""):
            st.session_state["openai_api_key"] = api_key_input
            st.rerun()

        if st.session_state.get("openai_api_key", "").strip():
            st.markdown(
                '<p style="font-size:0.72rem;color:#68d391;margin-top:0.2rem;">✓ API key set</p>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<p style="font-size:0.72rem;color:#fc8181;margin-top:0.2rem;">No key — AI features disabled</p>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown(
            '<div style="font-size:0.72rem;color:#64748b;text-align:center;padding-top:0.5rem;">'
            'VIDYA v1.0 · SDG 4: Quality Education</div>',
            unsafe_allow_html=True
        )

render_sidebar()

# ── Page router ────────────────────────────────────────────────────────────────
page = st.session_state.get("current_page", "Dashboard")

if page == "Dashboard":

    # ── Header ────────────────────────────────────────────────────────────────
    col_greeting, col_search = st.columns([5, 2])
    with col_greeting:
        st.markdown(
            '<h1 style="margin:0;font-size:1.9rem;font-weight:800;">Hello, Student! 👋</h1>'
            '<p style="margin:0;color:#6b7280;font-size:0.95rem;">Your learning journey, made accessible.</p>',
            unsafe_allow_html=True
        )

    with col_search:
        search_query = st.text_input("", placeholder="🔍  Search topics…", label_visibility="collapsed")

    st.markdown("---")

    # ── Quick actions ──────────────────────────────────────────────────────────
    st.markdown('<p class="vidya-section-title">⚡ Quick Actions</p>', unsafe_allow_html=True)
    qa1, qa2, qa3, qa4 = st.columns(4)
    with qa1:
        if st.button("📖 Continue Learning", use_container_width=True):
            st.session_state.current_page = "My Learning"
            st.rerun()
    with qa2:
        if st.button("🤖 Ask AI Tutor", use_container_width=True):
            st.session_state.current_page = "AI Tutor"
            st.rerun()
    with qa3:
        if st.button("🧠 Take a Quiz", use_container_width=True):
            st.session_state.current_page = "Quiz Center"
            st.rerun()
    with qa4:
        if st.button("📄 Read a Document", use_container_width=True):
            st.session_state.current_page = "Accessible Reader"
            st.rerun()

    st.markdown("---")

    # ── Main 3-column layout ───────────────────────────────────────────────────
    left_col, center_col, right_col = st.columns([1.4, 2.2, 1.4])

    # ── LEFT: Progress stats ────────────────────────────────────────────────────
    with left_col:
        st.markdown('<p class="vidya-section-title">📈 Learning Progress</p>', unsafe_allow_html=True)
        stats = pt.get_stats()

        st.metric("Lessons Completed", f"{stats['completed_lessons']} / {stats['total_lessons']}")
        st.progress(stats["completion_pct"] / 100)

        st.metric("Avg Quiz Score", f"{stats['avg_quiz_score']}%")
        score_pct = stats["avg_quiz_score"] / 100
        st.progress(min(score_pct, 1.0))

        st.metric("Study Hours (this week)", f"{stats['weekly_hours']} hrs")

        st.markdown("---")
        recs = pt.get_recommendations()
        if recs["revision"]:
            st.markdown('<p class="vidya-section-title">🔁 Needs Revision</p>', unsafe_allow_html=True)
            for topic in recs["revision"]:
                st.markdown(f"• {topic}")

    # ── CENTER: My Learning cards ───────────────────────────────────────────────
    with center_col:
        st.markdown('<p class="vidya-section-title">📚 My Learning</p>', unsafe_allow_html=True)

        lessons = db.get_lessons()

        badge_map = {
            "Science":          ("badge-science",  "🔬"),
            "Mathematics":      ("badge-math",     "📐"),
            "Computer Science": ("badge-cs",       "💻"),
            "Languages":        ("badge-lang",     "🗣️"),
        }

        # Group by subject
        subjects_shown = list(dict.fromkeys(l["subject"] for l in lessons))
        for subject in subjects_shown:
            subject_lessons = [l for l in lessons if l["subject"] == subject]
            completed = sum(1 for l in subject_lessons if l["completed"])
            total = len(subject_lessons)
            pct = int(completed / total * 100) if total else 0
            badge_cls, icon = badge_map.get(subject, ("badge-cs", "📌"))

            st.markdown(
                f'<div class="vidya-card">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">'
                f'<span style="font-weight:700;font-size:1rem;">{icon} {subject}</span>'
                f'<span class="vidya-badge {badge_cls}">{pct}% complete</span>'
                f'</div>'
                f'<p style="margin:0 0 0.6rem 0;font-size:0.85rem;color:#6b7280;">'
                f'{completed} of {total} lessons completed</p>',
                unsafe_allow_html=True
            )
            st.progress(pct / 100)
            if st.button(f"Continue → {subject}", key=f"continue_{subject}", use_container_width=True):
                st.session_state.current_page = "My Learning"
                st.session_state.selected_subject = subject
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ── RIGHT: AI Assistant card + accessibility tools ──────────────────────────
    with right_col:
        # Inclusive Learning Assistant card
        st.markdown(
            '<div class="vidya-card" style="background:linear-gradient(135deg,#ede9ff,#dbeafe);">'
            '<div style="text-align:center;margin-bottom:0.8rem;">'
            '<svg width="80" height="80" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">'
            '<circle cx="40" cy="40" r="38" fill="#7c6fcd" opacity="0.15"/>'
            '<circle cx="40" cy="30" r="14" fill="#7c6fcd"/>'
            '<circle cx="40" cy="30" r="8" fill="#fff"/>'
            '<circle cx="37" cy="28" r="2" fill="#7c6fcd"/>'
            '<circle cx="43" cy="28" r="2" fill="#7c6fcd"/>'
            '<path d="M24 58 Q40 44 56 58" stroke="#7c6fcd" stroke-width="3" fill="none" stroke-linecap="round"/>'
            '<line x1="40" y1="44" x2="40" y2="54" stroke="#7c6fcd" stroke-width="2.5"/>'
            '<line x1="40" y1="50" x2="33" y2="56" stroke="#7c6fcd" stroke-width="2.5" stroke-linecap="round"/>'
            '<line x1="40" y1="50" x2="47" y2="56" stroke="#7c6fcd" stroke-width="2.5" stroke-linecap="round"/>'
            '</svg></div>'
            '<h3 style="text-align:center;margin:0 0 0.4rem 0;font-size:1rem;font-weight:700;">Inclusive Learning Assistant</h3>'
            '<p style="text-align:center;font-size:0.82rem;color:#4b5563;margin-bottom:1rem;">'
            'Ask questions, get explanations, and learn in your own way.</p>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("🤖 Open AI Tutor", use_container_width=True):
            st.session_state.current_page = "AI Tutor"
            st.rerun()
        if st.button("📄 Open Accessible Reader", use_container_width=True):
            st.session_state.current_page = "Accessible Reader"
            st.rerun()

        st.markdown("---")
        st.markdown('<p class="vidya-section-title">♿ Accessibility Tools</p>', unsafe_allow_html=True)

        if st.button("✏️ Simplify Text", use_container_width=True):
            st.session_state.current_page = "Accessible Reader"
            st.session_state.reader_tab = "simplify"
            st.rerun()
        if st.button("🔊 Read Aloud", use_container_width=True):
            st.session_state.current_page = "Accessible Reader"
            st.session_state.reader_tab = "speech"
            st.rerun()
        if st.button("🌐 Translate Text", use_container_width=True):
            st.session_state.current_page = "Accessible Reader"
            st.session_state.reader_tab = "translate"
            st.rerun()

    st.markdown("---")

    # ── Bottom section ─────────────────────────────────────────────────────────
    bot_left, bot_right = st.columns(2)

    with bot_left:
        st.markdown('<p class="vidya-section-title">📅 Weekly Study Plan</p>', unsafe_allow_html=True)
        plan = pt.get_weekly_plan()
        if plan:
            for item in plan:
                st.markdown(
                    f'<div class="vidya-card" style="padding:0.7rem 1rem;margin-bottom:0.4rem;">'
                    f'<span style="font-weight:600;color:#7c6fcd;">{item["day"]}</span>'
                    f' &nbsp;·&nbsp; <span style="font-weight:500;">{item["subject"]}</span>'
                    f'<br><span style="font-size:0.82rem;color:#6b7280;">{item["task"]}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        else:
            st.info("All lessons complete! 🎉 Check Progress for details.")

    with bot_right:
        st.markdown('<p class="vidya-section-title">💡 Recommended Next Topics</p>', unsafe_allow_html=True)
        recs = pt.get_recommendations()
        if recs["suggested"]:
            for topic in recs["suggested"]:
                st.markdown(
                    f'<div class="vidya-card" style="padding:0.7rem 1rem;margin-bottom:0.4rem;">'
                    f'📌 {topic}'
                    f'</div>',
                    unsafe_allow_html=True
                )
        else:
            st.success("Great work — you're all caught up!")

# ── Route remaining pages to subpages ─────────────────────────────────────────
elif page == "My Learning":
    import pages.page_my_learning as _pg
    _pg.render()

elif page == "AI Tutor":
    import pages.page_ai_tutor as _pg
    _pg.render()

elif page == "Accessible Reader":
    import pages.page_accessible_reader as _pg
    _pg.render()

elif page == "Quiz Center":
    import pages.page_quiz_center as _pg
    _pg.render()

elif page == "Progress":
    import pages.page_progress as _pg
    _pg.render()

elif page == "Settings":
    import pages.page_settings as _pg
    _pg.render()
