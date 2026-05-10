"""
TalentScout Hiring Assistant Chatbot
A comprehensive hiring assistant built with Streamlit and Google Gemini.
Includes: User Auth (signup/login), CSV export, and session persistence.
"""

import streamlit as st
import json
import re
import csv
import io
from datetime import datetime
import config
import google.generativeai as genai
import hashlib
import auth  # local auth module

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

SYSTEM_PROMPT = config.SYSTEM_PROMPT
TECHNICAL_QUESTION_PROMPT = config.TECHNICAL_QUESTION_PROMPT
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
# HELPER FUNCTIONS
# ============================================================================

def is_exit_command(user_input: str) -> bool:
    user_lower = user_input.lower().strip()
    return any(keyword in user_lower for keyword in EXIT_KEYWORDS)


def extract_candidate_info(conversation_history: list) -> dict:
    conv_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
    try:
        response_text = call_gemini(
            system_instruction="You are a data extraction assistant. Extract candidate information from conversations and return valid JSON.",
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
    """Build a CSV string from the chat history and candidate info."""
    output = io.StringIO()
    writer = csv.writer(output)

    # Section 1: Candidate Info
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

    # Section 2: Chat History
    writer.writerow([])
    writer.writerow(["=== CHAT HISTORY ==="])
    writer.writerow(["#", "Role", "Message"])
    for i, msg in enumerate(messages, 1):
        writer.writerow([i, msg["role"].capitalize(), msg["content"]])

    return output.getvalue()


def reset_interview():
    st.session_state.messages = []
    st.session_state.candidate_info = {}
    st.session_state.conversation_phase = "greeting"
    st.session_state.tech_questions_generated = False
    st.session_state.conversation_concluded = False
    st.session_state.show_export = False


# ============================================================================
# AUTH PAGES
# ============================================================================

def render_auth_page():
    st.markdown("""
    <div class="top-navbar">
        <div class="logo">🎯 TalentScout Assistant</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; margin-bottom: 30px;">
        <h2 style="color:#e2e8f0;">Welcome to TalentScout</h2>
        <p style="color:#94a3b8;">Sign in or create an account to start interviewing candidates</p>
    </div>
    """, unsafe_allow_html=True)

    tab_login, tab_signup = st.tabs(["🔑 Login", "✨ Sign Up"])

    with tab_login:
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Login", use_container_width=True)

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
            new_email = st.text_input("Email", placeholder="your@email.com", key="su_email")
            new_password = st.text_input("Password", type="password", placeholder="Min. 6 characters", key="su_pass")
            new_password2 = st.text_input("Confirm Password", type="password", placeholder="Repeat password", key="su_pass2")
            submitted2 = st.form_submit_button("Create Account", use_container_width=True)

        if submitted2:
            if new_password != new_password2:
                st.error("Passwords do not match.")
            else:
                ok, msg = auth.signup(new_username, new_email, new_password)
                if ok:
                    st.success(msg + " Please log in.")
                else:
                    st.error(msg)


# ============================================================================
# MAIN CHAT APP
# ============================================================================

def render_chat_app():
    user = st.session_state.user

    # --- Guard: require API key ---
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
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'candidate_info' not in st.session_state:
        st.session_state.candidate_info = {}
    if 'conversation_phase' not in st.session_state:
        st.session_state.conversation_phase = "greeting"
    if 'tech_questions_generated' not in st.session_state:
        st.session_state.tech_questions_generated = False
    if 'conversation_concluded' not in st.session_state:
        st.session_state.conversation_concluded = False
    if 'show_export' not in st.session_state:
        st.session_state.show_export = False

    # ---- TOP NAVBAR ----
    st.markdown(f"""
    <div class="top-navbar">
        <div class="logo">🎯 TalentScout Assistant</div>
        <div style="color:#94a3b8; font-size:0.9rem;">Logged in as <strong style="color:#e2e8f0;">{user['username']}</strong></div>
    </div>
    """, unsafe_allow_html=True)

    # ---- SIDEBAR ----
    with st.sidebar:
        st.markdown("⚙️ **Actions**")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔄 Reset Chat", use_container_width=True):
                reset_interview()
                st.rerun()

        with col2:
            if st.button("📥 Export", use_container_width=True):
                st.session_state.show_export = True

        if st.button("📄 View Report", use_container_width=True):
            st.session_state.show_export = True

        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        # Past sessions
        st.markdown("### 📂 Past Sessions")
        sessions = auth.get_user_sessions(user["id"])
        if sessions:
            for s in sessions[:5]:
                dt = s["session_date"][:10]
                name = s["candidate_name"] or "Unnamed"
                st.markdown(f"<div class='sidebar-phase'>📋 {name} — {dt}</div>", unsafe_allow_html=True)
        else:
            st.caption("No past sessions yet.")

    # ---- SESSION HEADER ----
    cand_name = st.session_state.candidate_info.get("full_name", "Candidate")
    cand_role = st.session_state.candidate_info.get("desired_positions", "Tech Role")
    st.markdown(f"""
    <div class="session-header">
        <h3>Session: Technical Screening with</h3>
        <div class="candidate-badge">
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed={cand_name}" alt="Candidate"/>
            <div class="cand-info">
                <span class="cand-name">{cand_name}</span>
                <span class="cand-role">{cand_role}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- CHAT MESSAGES ----
    chat_container = st.container()
    with chat_container:
        if not st.session_state.messages:
            st.markdown("<div style='color:#64748b; text-align:center; padding:40px 0;'>👋 The interview will begin when the candidate sends their first message.</div>", unsafe_allow_html=True)
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    # ---- INPUT AREA ----
    if not st.session_state.conversation_concluded:
        user_input = st.chat_input("Type your response here...", key="user_input")

        if user_input:
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

                # Auto-save session to DB
                auth.save_session(user["id"], user["username"], st.session_state.messages, candidate_info)
                st.rerun()

            st.session_state.messages.append({"role": "user", "content": user_input})

            try:
                with st.spinner("🤔 Processing your response..."):
                    history = convert_to_gemini_history(st.session_state.messages[:-1])
                    assistant_message = call_gemini(
                        system_instruction=SYSTEM_PROMPT,
                        user_message=user_input,
                        history=history if history else None
                    )
                    st.session_state.messages.append({"role": "assistant", "content": assistant_message})

                    if len(st.session_state.messages) % 6 == 0:
                        st.session_state.candidate_info = extract_candidate_info(st.session_state.messages)
                    st.rerun()

            except Exception as e:
                st.error(f"❌ Error processing request: {str(e)}")
                st.session_state.messages.pop()

    else:
        st.markdown("""
        <div class="success-msg">
            <h4>✅ Interview Concluded</h4>
            <p>Session saved to your account. Download the data below or start a new interview.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔄 Start New Interview"):
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
            # CSV Export
            csv_data = build_csv_export(st.session_state.messages, candidate_info)
            st.download_button(
                label="📊 Download CSV",
                data=csv_data,
                file_name=f"{fname_base}_interview.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col_b:
            # JSON Export
            export_data = {
                "candidate_info": candidate_info,
                "conversation_messages": len(st.session_state.messages),
                "session_date": datetime.now().isoformat(),
                "interview_type": "Initial Screening",
                "messages": st.session_state.messages
            }
            st.download_button(
                label="📦 Download JSON",
                data=json.dumps(export_data, indent=2),
                file_name=f"{fname_base}_interview.json",
                mime="application/json",
                use_container_width=True
            )

        with col_c:
            # Markdown Export
            st.download_button(
                label="📄 Download Report",
                data=summary,
                file_name=f"{fname_base}_summary.md",
                mime="text/markdown",
                use_container_width=True
            )

        st.markdown(summary)


# ============================================================================
# APP ENTRY POINT — AUTH GATE
# ============================================================================

def main():
    # Initialise auth state
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