"""Main Streamlit application file for HireBot UI."""
import streamlit as st
from dotenv import load_dotenv

from chatbot import HireBotChatbot
from utils import format_interview_summary
from config import APP_NAME, APP_SUBTITLE

load_dotenv()

st.set_page_config(
    page_title=f"{APP_NAME} | {APP_SUBTITLE}",
    page_icon="🎯",
    layout="wide"
)

THEMES = {
    "dark": {
        "bg":         "#212121",
        "sidebar_bg": "#171717",
        "msg_user":   "#2f2f2f",
        "msg_bot":    "#1a1a1a",
        "input_bg":   "#2f2f2f",
        "border":     "#444444",
        "text":       "#ececec",
        "subtext":    "#999999",
        "accent":     "#10a37f",
        "tag_bg":     "#1e3a30",
        "tag_text":   "#10a37f",
        "icon":       "🌙",
        "next":       "light",
        "label":      "Switch to Light",
    },
    "light": {
        "bg":         "#f9f9f9",
        "sidebar_bg": "#f0f0f0",
        "msg_user":   "#e8e8e8",
        "msg_bot":    "#ffffff",
        "input_bg":   "#ffffff",
        "border":     "#dddddd",
        "text":       "#111111",
        "subtext":    "#666666",
        "accent":     "#10a37f",
        "tag_bg":     "#d9f0ea",
        "tag_text":   "#0a7a5e",
        "icon":       "☀️",
        "next":       "midnight",
        "label":      "Switch to Midnight",
    },
    "midnight": {
        "bg":         "#0d1117",
        "sidebar_bg": "#090d13",
        "msg_user":   "#161b22",
        "msg_bot":    "#0d1117",
        "input_bg":   "#161b22",
        "border":     "#30363d",
        "text":       "#c9d1d9",
        "subtext":    "#8b949e",
        "accent":     "#58a6ff",
        "tag_bg":     "#1a2a40",
        "tag_text":   "#58a6ff",
        "icon":       "🌌",
        "next":       "dark",
        "label":      "Switch to Dark",
    },
}


def init_session():
    if "theme" not in st.session_state:
        st.session_state.theme = "midnight"
    if "bot" not in st.session_state:
        st.session_state.bot = HireBotChatbot()
        st.session_state.messages = []
        greeting = st.session_state.bot.get_initial_greeting()
        st.session_state.messages.append({"role": "assistant", "content": greeting})
    if "input_key" not in st.session_state:
        st.session_state.input_key = 0


def apply_theme(t: dict):
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

        html, body, .stApp, [class*="css"] {{
            font-family: 'Inter', sans-serif !important;
            background-color: {t['bg']} !important;
            color: {t['text']} !important;
        }}

        /* ── Hide Streamlit chrome ── */
        #MainMenu, footer {{ visibility: hidden; }}
        header[data-testid="stHeader"] {{ background: transparent !important; }}

        /* ── Hide the default floating bottom bar entirely ── */
        section[data-testid="stBottom"] {{
            display: none !important;
        }}

        /* ── Main block ── */
        .block-container {{
            max-width: 820px;
            margin: 0 auto;
            padding-top: 1rem;
            padding-bottom: 2rem;
            background-color: {t['bg']} !important;
        }}

        /* ── Sidebar ── */
        [data-testid="stSidebar"] > div:first-child {{
            background-color: {t['sidebar_bg']} !important;
            border-right: 1px solid {t['border']};
        }}
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] div {{
            color: {t['text']} !important;
        }}

        /* Sidebar collapse arrow always visible */
        [data-testid="collapsedControl"] {{
            background-color: {t['accent']} !important;
            border-radius: 0 8px 8px 0 !important;
            opacity: 1 !important;
            visibility: visible !important;
        }}
        [data-testid="collapsedControl"] svg {{
            fill: white !important;
        }}

        /* ── All text ── */
        p, span, li, div, label {{
            color: {t['text']} !important;
        }}

        /* ── Chat messages ── */
        [data-testid="stChatMessage"] {{
            border-radius: 12px !important;
            padding: 0.8rem 1rem !important;
            margin-bottom: 0.5rem !important;
            border: 1px solid {t['border']} !important;
        }}
        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {{
            background-color: {t['msg_user']} !important;
        }}
        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {{
            background-color: {t['msg_bot']} !important;
        }}
        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] span,
        [data-testid="stChatMessage"] div,
        [data-testid="stChatMessage"] li,
        [data-testid="stChatMessage"] strong {{
            color: {t['text']} !important;
        }}

        /* ── Custom inline input box ── */
        .chat-input-wrapper {{
            display: flex;
            align-items: center;
            gap: 10px;
            background-color: {t['input_bg']};
            border: 1.5px solid {t['border']};
            border-radius: 14px;
            padding: 8px 12px;
            margin-top: 1rem;
            box-shadow: 0 2px 12px rgba(0,0,0,0.15);
        }}
        .chat-input-wrapper:focus-within {{
            border-color: {t['accent']};
            box-shadow: 0 0 0 2px {t['accent']}33;
        }}

        /* Override Streamlit text_input inside our wrapper */
        .chat-input-wrapper [data-testid="stTextInput"] {{
            flex: 1;
        }}
        .chat-input-wrapper [data-testid="stTextInput"] input {{
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            color: {t['text']} !important;
            font-size: 1rem !important;
            padding: 4px 0 !important;
        }}
        .chat-input-wrapper [data-testid="stTextInput"] input::placeholder {{
            color: {t['subtext']} !important;
        }}
        .chat-input-wrapper [data-testid="stTextInput"] > div {{
            border: none !important;
            background: transparent !important;
        }}

        /* Send button inside wrapper */
        .send-btn > button {{
            background-color: {t['accent']} !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.4rem 1rem !important;
            font-size: 1rem !important;
            min-width: 42px;
        }}
        .send-btn > button:hover {{
            opacity: 0.85 !important;
        }}

        /* ── Progress bar ── */
        .stProgress > div > div > div > div {{
            background-color: {t['accent']} !important;
        }}
        .stProgress > div > div > div {{
            background-color: {t['border']} !important;
        }}

        /* ── Buttons ── */
        .stButton > button {{
            background-color: transparent !important;
            border: 1px solid {t['border']} !important;
            color: {t['text']} !important;
            border-radius: 8px !important;
            transition: all 0.2s;
        }}
        .stButton > button:hover {{
            background-color: {t['accent']} !important;
            border-color: {t['accent']} !important;
            color: white !important;
        }}

        /* Theme toggle pill */
        .theme-btn > button {{
            background-color: {t['accent']} !important;
            border: none !important;
            color: white !important;
            border-radius: 20px !important;
            font-size: 1rem !important;
        }}

        /* Download button */
        .stDownloadButton > button {{
            background-color: {t['accent']} !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
        }}

        /* Alert / info box */
        .stAlert {{
            background-color: {t['msg_bot']} !important;
            color: {t['text']} !important;
            border: 1px solid {t['border']} !important;
            border-radius: 10px !important;
        }}

        hr {{ border-color: {t['border']} !important; }}
        .stCaption, small {{ color: {t['subtext']} !important; }}

        /* Sidebar labels */
        .sidebar-label {{
            font-size: 0.68rem;
            font-weight: 600;
            letter-spacing: 0.09em;
            text-transform: uppercase;
            color: {t['subtext']} !important;
            margin: 0.8rem 0 0.3rem 0;
        }}

        .profile-tag {{
            display: block;
            background: {t['tag_bg']};
            color: {t['tag_text']} !important;
            border-radius: 6px;
            padding: 4px 10px;
            font-size: 0.8rem;
            margin: 3px 0;
        }}

        .stage-badge {{
            display: inline-block;
            background: {t['tag_bg']};
            color: {t['tag_text']} !important;
            border-radius: 20px;
            padding: 3px 12px;
            font-size: 0.78rem;
            font-weight: 500;
        }}

        /* Header */
        .ts-header {{
            display: flex;
            align-items: center;
            padding-bottom: 12px;
            border-bottom: 2px solid {t['accent']};
            margin-bottom: 1.2rem;
        }}
        .ts-title {{
            font-size: 1.5rem;
            font-weight: 600;
            color: {t['accent']} !important;
            margin: 0;
        }}
        .ts-sub {{
            font-size: 0.82rem;
            color: {t['subtext']} !important;
            margin: 0;
        }}

        ::-webkit-scrollbar {{ width: 5px; }}
        ::-webkit-scrollbar-track {{ background: {t['bg']}; }}
        ::-webkit-scrollbar-thumb {{ background: {t['border']}; border-radius: 3px; }}
    </style>
    """, unsafe_allow_html=True)


def main():
    init_session()
    bot: HireBotChatbot = st.session_state.bot
    t = THEMES[st.session_state.theme]
    apply_theme(t)

    # ── SIDEBAR ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown('<p class="sidebar-label">Progress</p>', unsafe_allow_html=True)
        st.progress(bot.get_progress_percentage() / 100.0)
        st.markdown(
            f'<span class="stage-badge">📍 {bot.stage.replace("_", " ").title()}</span>',
            unsafe_allow_html=True
        )
        st.markdown("---")

        st.markdown('<p class="sidebar-label">Profile Summary</p>', unsafe_allow_html=True)
        icons = {"name": "👤", "email": "📧", "phone": "📞",
                 "experience": "🏅", "position": "💼", "location": "📍"}
        any_info = any(v for v in bot.candidate_info.values())
        if any_info:
            for key, val in bot.candidate_info.items():
                if val:
                    st.markdown(
                        f'<span class="profile-tag">{icons.get(key,"•")} <b>{key.title()}:</b> {val}</span>',
                        unsafe_allow_html=True
                    )
        else:
            st.caption("No info collected yet.")

        st.markdown("---")

        if bot.qa_pairs:
            summary_text = format_interview_summary(bot.candidate_info, bot.qa_pairs)
            st.download_button(
                "📥 Download Summary", data=summary_text,
                file_name="HireBot_Summary.txt", mime="text/plain",
                use_container_width=True
            )

        if st.button("🔄 New Session", use_container_width=True):
            theme_backup = st.session_state.theme
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.theme = theme_backup
            st.rerun()

    # ── HEADER ────────────────────────────────────────────────────────────────
    col_title, col_btn = st.columns([7, 1])
    with col_title:
        st.markdown(f"""
        <div class="ts-header">
            <span style="font-size:1.8rem;margin-right:12px;">🎯</span>
            <div>
                <p class="ts-title">HireBot</p>
                <p class="ts-sub">AI Hiring Assistant · LLaMA 3.3 70B</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_btn:
        st.markdown('<div class="theme-btn">', unsafe_allow_html=True)
        if st.button(t['icon'], help=t['label'], use_container_width=True):
            st.session_state.theme = t['next']
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── CHAT MESSAGES ─────────────────────────────────────────────────────────
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ── CUSTOM INLINE INPUT ───────────────────────────────────────────────────
    if bot.stage != "FAREWELL":
        st.markdown('<div class="chat-input-wrapper">', unsafe_allow_html=True)
        col_input, col_send = st.columns([11, 1])
        with col_input:
            user_input = st.text_input(
                label="chat",
                placeholder="Message HireBot...",
                label_visibility="collapsed",
                key=f"chat_input_{st.session_state.input_key}"
            )
        with col_send:
            st.markdown('<div class="send-btn">', unsafe_allow_html=True)
            send_clicked = st.button("➤", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        message = st.session_state.get(f"chat_input_{st.session_state.input_key}", "").strip()
        if (send_clicked or user_input) and message:
            previous_stage = bot.stage

            with st.chat_message("user"):
                st.markdown(message)
            st.session_state.messages.append({"role": "user", "content": message})

            with st.chat_message("assistant"):
                with st.spinner(""):
                    bot_response = bot.process_message(message)
                st.markdown(bot_response)
            st.session_state.messages.append({"role": "assistant", "content": bot_response})

            if previous_stage != bot.stage and bot.stage != "FAREWELL":
                st.toast(f"✅ {bot.stage.replace('_', ' ').title()}", icon="💾")

            # Increment key to force a fresh empty input widget
            st.session_state.input_key += 1
            st.rerun()
    else:
        st.info("✅ Interview complete. Download your summary from the sidebar or start a new session.")


if __name__ == "__main__":
    main()
