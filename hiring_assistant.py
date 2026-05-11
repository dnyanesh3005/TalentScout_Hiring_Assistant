"""
TalentScout Hiring Assistant Chatbot — v2.0
Advanced features: Sentiment Analysis, Multilingual Support,
Personalized Responses, Premium UI.
"""

import streamlit as st
import json
import re
import csv
import io
from datetime import datetime
import config
import google.generativeai as genai
import auth
from features import (
    analyze_sentiment, get_sentiment_history_summary,
    get_multilingual_system_prompt, build_personalized_context,
    SUPPORTED_LANGUAGES,
)

# ============================================================================
# PAGE CONFIG (MUST be first Streamlit call)
# ============================================================================
st.set_page_config(**config.PAGE_CONFIG)
st.markdown(config.CUSTOM_CSS, unsafe_allow_html=True)

# ============================================================================
# INITIALIZE GEMINI
# ============================================================================
genai.configure(api_key=config.GEMINI_API_KEY)

generation_config = genai.types.GenerationConfig(
    max_output_tokens=config.MAX_TOKENS,
    temperature=config.TEMPERATURE,
)

EXIT_KEYWORDS = config.EXIT_KEYWORDS


# ============================================================================
# GEMINI HELPERS
# ============================================================================

def call_gemini(system_instruction: str, user_message: str, history: list = None) -> str:
    model = genai.GenerativeModel(
        model_name=config.MODEL,
        system_instruction=system_instruction,
        generation_config=generation_config,
    )
    if history:
        chat = model.start_chat(history=history)
        response = chat.send_message(user_message)
    else:
        response = model.generate_content(user_message)
    return response.text


def convert_to_gemini_history(messages: list) -> list:
    gemini_history = []
    for msg in messages:
        role = "model" if msg["role"] == "assistant" else "user"
        gemini_history.append({"role": role, "parts": [msg["content"]]})
    return gemini_history


# ============================================================================
# HELPERS
# ============================================================================

def is_exit_command(user_input: str) -> bool:
    user_lower = user_input.lower().strip()
    return any(keyword in user_lower for keyword in EXIT_KEYWORDS)


def extract_candidate_info(conversation_history: list) -> dict:
    conv_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
    try:
        response_text = call_gemini(
            system_instruction="You are a data extraction assistant. Extract candidate information and return valid JSON.",
            user_message=config.CANDIDATE_INFO_EXTRACTION_PROMPT.format(conversation_text=conv_text)
        )
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        st.warning(f"Could not extract structured data: {str(e)}")
    return {}


def format_conversation_summary(messages: list, candidate_info: dict) -> str:
    tech_stack = candidate_info.get('tech_stack', [])
    tech_str = ', '.join(tech_stack) if isinstance(tech_stack, list) else str(tech_stack)
    return f"""
**CANDIDATE INTERVIEW SUMMARY**
================================

**Candidate Information:**
- Name: {candidate_info.get('full_name', 'Not provided')}
- Email: {candidate_info.get('email', 'Not provided')}
- Phone: {candidate_info.get('phone', 'Not provided')}
- Experience: {candidate_info.get('years_of_experience', 'Not provided')} years
- Desired Position(s): {candidate_info.get('desired_positions', 'Not provided')}
- Location: {candidate_info.get('current_location', 'Not provided')}
- Tech Stack: {tech_str}

**Interview Duration:** {len(messages)} messages exchanged
**Interview Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Next Steps:**
1. Review candidate's technical assessment responses
2. Schedule technical interview if qualified
3. Contact candidate via provided communication channels
"""


def build_csv_export(messages: list, candidate_info: dict) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["=== CANDIDATE INFORMATION ==="])
    writer.writerow(["Field", "Value"])
    info_fields = [
        ("Full Name", candidate_info.get("full_name", "")),
        ("Email", candidate_info.get("email", "")),
        ("Phone", candidate_info.get("phone", "")),
        ("Years of Experience", candidate_info.get("years_of_experience", "")),
        ("Desired Positions", candidate_info.get("desired_positions", "")),
        ("Current Location", candidate_info.get("current_location", "")),
        ("Tech Stack", ", ".join(candidate_info.get("tech_stack", [])) if isinstance(candidate_info.get("tech_stack"), list) else str(candidate_info.get("tech_stack", ""))),
        ("Interview Date", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        ("Total Messages", len(messages)),
    ]
    for field, value in info_fields:
        writer.writerow([field, value])
    writer.writerow([])
    writer.writerow(["=== CHAT HISTORY ==="])
    writer.writerow(["#", "Role", "Message", "Sentiment"])
    sentiments = st.session_state.get("sentiment_history", [])
    user_msg_idx = 0
    for i, msg in enumerate(messages, 1):
        sentiment_label = ""
        if msg["role"] == "user" and user_msg_idx < len(sentiments):
            sentiment_label = sentiments[user_msg_idx].get("label", "")
            user_msg_idx += 1
        writer.writerow([i, msg["role"].capitalize(), msg["content"], sentiment_label])
    return output.getvalue()


def reset_interview():
    st.session_state.messages = []
    st.session_state.candidate_info = {}
    st.session_state.conversation_phase = "greeting"
    st.session_state.tech_questions_generated = False
    st.session_state.conversation_concluded = False
    st.session_state.show_export = False
    st.session_state.sentiment_history = []


def render_progress_tracker(phase: str):
    phases = [
        ("greeting", "👋", "Greeting"),
        ("info_gathering", "📝", "Info Gathering"),
        ("technical_assessment", "🧠", "Tech Assessment"),
        ("concluded", "✅", "Concluded"),
    ]
    phase_order = [p[0] for p in phases]
    current_idx = phase_order.index(phase) if phase in phase_order else 0

    steps_html = ""
    for i, (key, icon, label) in enumerate(phases):
        if i < current_idx:
            state = "done"
            dot_content = "✓"
        elif i == current_idx:
            state = "active"
            dot_content = icon
        else:
            state = "pending"
            dot_content = str(i + 1)

        step_html = f"""
        <div class="progress-step">
            <div class="step-dot {state}">{dot_content}</div>
            <span class="step-label {state}">{label}</span>
        </div>"""
        if i < len(phases) - 1:
            step_html += '<div class="step-connector"></div>'
        steps_html += step_html

    st.markdown(f'<div class="progress-tracker">{steps_html}</div>', unsafe_allow_html=True)


def render_sentiment_sidebar(sentiment_history: list):
    if not sentiment_history:
        return
    summary = get_sentiment_history_summary(sentiment_history)
    dominant = summary["dominant"]
    trend_icon = {"improving": "📈", "declining": "📉", "stable": "➡️"}.get(summary["trend"], "➡️")

    st.markdown(f"""
    <div class="sentiment-card">
        <span class="big-emoji">{dominant['emoji']}</span>
        <div class="sent-label">{dominant['label']}</div>
        <div class="sent-sub">Mood trend: {trend_icon} {summary['trend'].title()}</div>
    </div>
    """, unsafe_allow_html=True)

    # Mini bar breakdown
    counts = summary.get("counts", {})
    if counts:
        for label, count in sorted(counts.items(), key=lambda x: -x[1])[:3]:
            pct = int(count / len(sentiment_history) * 100)
            info = next((v for v in __import__('features').SENTIMENT_LABELS.values() if v["label"] == label), None)
            if info:
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">'
                    f'<span style="font-size:0.8rem;width:70px;color:#94a3b8;">{info["emoji"]} {label}</span>'
                    f'<div style="flex:1;background:#1f2236;border-radius:4px;height:6px;">'
                    f'<div style="width:{pct}%;background:{info["color"]};border-radius:4px;height:100%;"></div>'
                    f'</div><span style="font-size:0.7rem;color:#64748b;">{pct}%</span></div>',
                    unsafe_allow_html=True
                )


# ============================================================================
# AUTH PAGES — Premium Design
# ============================================================================

def render_auth_page():
    # Centered layout
    _, col, _ = st.columns([1, 1.4, 1])
    with col:
        st.markdown("""
        <div class="auth-card">
            <div class="auth-hero">
                <span class="hero-icon">🎯</span>
                <h1>TalentScout</h1>
                <p>AI-powered hiring assistant for modern recruiters</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        tab_login, tab_signup = st.tabs(["🔑 Sign In", "✨ Create Account"])

        with tab_login:
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                submitted = st.form_submit_button("Sign In →", use_container_width=True)
            if submitted:
                ok, msg, user = auth.login(username, password)
                if ok:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        with tab_signup:
            with st.form("signup_form"):
                new_username = st.text_input("Username", placeholder="Choose a username", key="su_user")
                new_email    = st.text_input("Email", placeholder="your@email.com", key="su_email")
                new_password = st.text_input("Password", type="password", placeholder="Min. 6 characters", key="su_pass")
                new_password2= st.text_input("Confirm Password", type="password", placeholder="Repeat password", key="su_pass2")
                submitted2   = st.form_submit_button("Create Account →", use_container_width=True)
            if submitted2:
                if new_password != new_password2:
                    st.error("Passwords do not match.")
                else:
                    ok, msg = auth.signup(new_username, new_email, new_password)
                    if ok:
                        st.success(msg + " Please sign in.")
                    else:
                        st.error(msg)

        st.markdown("""
        <div style="text-align:center;margin-top:24px;color:#475569;font-size:0.75rem;">
            🔒 Secure · AI-Powered · Professional Hiring
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# MAIN CHAT APP
# ============================================================================

def render_chat_app():
    user = st.session_state.user

    if not config.GEMINI_API_KEY:
        st.error(
            "⚠️ **GEMINI_API_KEY is missing!**\n\n"
            "1. Go to https://aistudio.google.com/app/apikey\n"
            "2. Create a free API key\n"
            "3. Add `GEMINI_API_KEY=your_key_here` to your `.env` file\n"
            "4. Restart the app"
        )
        st.stop()

    # --- Init session state ---
    defaults = {
        "messages": [],
        "candidate_info": {},
        "conversation_phase": "greeting",
        "tech_questions_generated": False,
        "conversation_concluded": False,
        "show_export": False,
        "sentiment_history": [],
        "selected_language": "English",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # ---- TOP NAVBAR ----
    past_sessions = auth.get_user_sessions(user["id"])
    session_count = len(past_sessions)
    st.markdown(f"""
    <div class="top-navbar">
        <div class="logo">
            <span class="logo-icon">🎯</span>
            TalentScout
            <span class="nav-badge">AI Hiring Assistant</span>
        </div>
        <div style="display:flex;align-items:center;gap:14px;">
            <span style="color:#64748b;font-size:0.8rem;">👤 <strong style="color:#e2e8f0;">{user['username']}</strong></span>
            <span style="color:#64748b;font-size:0.8rem;">📂 {session_count} session{'s' if session_count != 1 else ''}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- SIDEBAR ----
    with st.sidebar:
        # Language selector
        st.markdown("### 🌐 Language")
        lang_options = list(SUPPORTED_LANGUAGES.keys())
        lang_display = [f"{SUPPORTED_LANGUAGES[l]['flag']} {l}" for l in lang_options]
        current_lang_idx = lang_options.index(st.session_state.selected_language)
        selected_display = st.selectbox(
            "Interview Language",
            lang_display,
            index=current_lang_idx,
            label_visibility="collapsed",
        )
        new_lang = lang_options[lang_display.index(selected_display)]
        if new_lang != st.session_state.selected_language:
            st.session_state.selected_language = new_lang
            st.rerun()

        st.divider()

        # Sentiment analysis panel
        if config.FEATURES["sentiment_analysis"] and st.session_state.sentiment_history:
            st.markdown("### 🧠 Sentiment Analysis")
            render_sentiment_sidebar(st.session_state.sentiment_history)
            st.divider()

        # Actions
        st.markdown("### ⚙️ Actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Reset", use_container_width=True):
                reset_interview()
                st.rerun()
        with col2:
            if st.button("📊 Export", use_container_width=True):
                st.session_state.show_export = True

        if st.button("📄 View Report", use_container_width=True):
            st.session_state.show_export = True

        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        # Stats
        msg_count = len(st.session_state.messages)
        user_msgs = sum(1 for m in st.session_state.messages if m["role"] == "user")
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:4px;">
            <div class="stat-card">
                <div class="stat-value">{msg_count}</div>
                <div class="stat-label">Messages</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{user_msgs}</div>
                <div class="stat-label">Responses</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Past sessions
        st.markdown("### 📂 Past Sessions")
        if past_sessions:
            for s in past_sessions[:5]:
                dt   = s["session_date"][:10]
                name = s["candidate_name"] or "Unnamed"
                st.markdown(f"<div class='sidebar-phase'>📋 {name} — {dt}</div>", unsafe_allow_html=True)
        else:
            st.caption("No past sessions yet.")

    # ---- PROGRESS TRACKER ----
    render_progress_tracker(st.session_state.conversation_phase)

    # ---- SESSION HEADER ----
    cand_name = st.session_state.candidate_info.get("full_name", "Candidate")
    cand_role = st.session_state.candidate_info.get("desired_positions", "Tech Role")
    lang_info = SUPPORTED_LANGUAGES[st.session_state.selected_language]
    st.markdown(f"""
    <div class="session-header">
        <h3>Technical Screening</h3>
        <div class="candidate-badge">
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed={cand_name}" alt="Candidate"/>
            <div class="cand-info">
                <span class="cand-name">{cand_name}</span>
                <span class="cand-role">{cand_role}</span>
            </div>
        </div>
        <span style="margin-left:auto;font-size:0.8rem;color:#64748b;">
            {lang_info['flag']} {st.session_state.selected_language}
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ---- CHAT MESSAGES ----
    with st.container():
        if not st.session_state.messages:
            st.markdown(
                "<div style='color:#475569;text-align:center;padding:48px 0;font-size:0.95rem;'>"
                "👋 The interview begins when the candidate sends their first message.</div>",
                unsafe_allow_html=True
            )

        sentiment_idx = 0
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                # Show sentiment badge on user messages
                if (
                    message["role"] == "user"
                    and config.FEATURES["sentiment_analysis"]
                    and sentiment_idx < len(st.session_state.sentiment_history)
                ):
                    sent = st.session_state.sentiment_history[sentiment_idx]
                    badge_color = sent.get("color", "#64748b")
                    st.markdown(
                        f'{message["content"]}'
                        f'<span class="sentiment-badge" style="background:{badge_color}22;color:{badge_color};border:1px solid {badge_color}44;">'
                        f'{sent["emoji"]} {sent["label"]}</span>',
                        unsafe_allow_html=True
                    )
                    sentiment_idx += 1
                else:
                    st.write(message["content"])
                    if message["role"] == "user":
                        sentiment_idx += 1

    # ---- INPUT AREA ----
    if not st.session_state.conversation_concluded:
        user_input = st.chat_input(
            f"Type in {st.session_state.selected_language}...",
            key="user_input"
        )

        if user_input:
            # Build personalised + multilingual system prompt
            personalisation = build_personalized_context(past_sessions)
            system_prompt = get_multilingual_system_prompt(
                config.SYSTEM_PROMPT + personalisation,
                st.session_state.selected_language
            )

            # Exit handling
            if is_exit_command(user_input):
                st.session_state.messages.append({"role": "user", "content": user_input})
                candidate_info = extract_candidate_info(st.session_state.messages)
                st.session_state.candidate_info = candidate_info

                conclusion_response = config.CONCLUSION_TEMPLATE.format(
                    name=candidate_info.get('full_name', 'Not provided'),
                    experience=candidate_info.get('years_of_experience', 'Not provided'),
                    tech_stack=', '.join(candidate_info.get('tech_stack', [])) if candidate_info.get('tech_stack') else 'Not specified',
                    position=candidate_info.get('desired_positions', 'Not specified'),
                    email=candidate_info.get('email', 'your email'),
                    phone=candidate_info.get('phone', 'phone')
                )
                st.session_state.messages.append({"role": "assistant", "content": conclusion_response})
                st.session_state.conversation_concluded = True
                st.session_state.conversation_phase = "concluded"
                auth.save_session(user["id"], user["username"], st.session_state.messages, candidate_info)
                st.rerun()

            st.session_state.messages.append({"role": "user", "content": user_input})

            # Async sentiment analysis
            if config.FEATURES["sentiment_analysis"]:
                with st.spinner(""):
                    sentiment = analyze_sentiment(user_input)
                    st.session_state.sentiment_history.append(sentiment)

            try:
                with st.spinner("🤔 Processing your response..."):
                    history = convert_to_gemini_history(st.session_state.messages[:-1])
                    assistant_message = call_gemini(
                        system_instruction=system_prompt,
                        user_message=user_input,
                        history=history if history else None
                    )
                    st.session_state.messages.append({"role": "assistant", "content": assistant_message})

                    # Update conversation phase heuristic
                    msg_count = len(st.session_state.messages)
                    if msg_count <= 4:
                        st.session_state.conversation_phase = "greeting"
                    elif msg_count <= 14:
                        st.session_state.conversation_phase = "info_gathering"
                    else:
                        st.session_state.conversation_phase = "technical_assessment"

                    if msg_count % 6 == 0:
                        st.session_state.candidate_info = extract_candidate_info(st.session_state.messages)

                    st.rerun()

            except Exception as e:
                st.error(f"❌ Error processing request: {str(e)}")
                st.session_state.messages.pop()

    else:
        st.markdown("""
        <div class="success-msg">
            <h4>✅ Interview Concluded</h4>
            <p>Session saved. Download the report below or start a new interview.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 Start New Interview", use_container_width=True):
            reset_interview()
            st.rerun()

    # ---- EXPORT PANEL ----
    if st.session_state.show_export and st.session_state.messages:
        st.divider()
        st.markdown("### 📊 Export Interview Data")

        candidate_info = extract_candidate_info(st.session_state.messages)
        st.session_state.candidate_info = candidate_info
        summary = format_conversation_summary(st.session_state.messages, candidate_info)
        fname_base = candidate_info.get('full_name', 'candidate').replace(' ', '_')

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            csv_data = build_csv_export(st.session_state.messages, candidate_info)
            st.download_button("📊 Download CSV", csv_data, f"{fname_base}_interview.csv", "text/csv", use_container_width=True)
        with col_b:
            export_data = {
                "candidate_info": candidate_info,
                "conversation_messages": len(st.session_state.messages),
                "session_date": datetime.now().isoformat(),
                "interview_type": "Initial Screening",
                "language": st.session_state.selected_language,
                "sentiment_history": [s.get("label") for s in st.session_state.sentiment_history],
                "messages": st.session_state.messages
            }
            st.download_button("📦 Download JSON", json.dumps(export_data, indent=2), f"{fname_base}_interview.json", "application/json", use_container_width=True)
        with col_c:
            st.download_button("📄 Download Report", summary, f"{fname_base}_summary.md", "text/markdown", use_container_width=True)

        st.markdown(summary)


# ============================================================================
# APP ENTRY POINT — AUTH GATE
# ============================================================================

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user" not in st.session_state:
        st.session_state.user = {}

    if not st.session_state.logged_in:
        render_auth_page()
    else:
        render_chat_app()


if __name__ == "__main__":
    main()