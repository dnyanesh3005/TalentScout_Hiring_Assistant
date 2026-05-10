"""
TalentScout Hiring Assistant Chatbot
A comprehensive hiring assistant built with Streamlit and Google Gemini (Free LLM)
"""

import streamlit as st
import json
import re
from datetime import datetime
import config
import google.generativeai as genai
import hashlib

# ============================================================================
# INITIALIZE GOOGLE GEMINI CLIENT (Free API)
# ============================================================================

genai.configure(api_key=config.GEMINI_API_KEY)

# Gemini generation config
generation_config = genai.types.GenerationConfig(
    max_output_tokens=config.MAX_TOKENS,
    temperature=config.TEMPERATURE,
)

# Page configuration
st.set_page_config(**config.PAGE_CONFIG)

# Custom CSS for professional styling
st.markdown(config.CUSTOM_CSS, unsafe_allow_html=True)

# Constants from config
SYSTEM_PROMPT = config.SYSTEM_PROMPT
TECHNICAL_QUESTION_PROMPT = config.TECHNICAL_QUESTION_PROMPT
EXIT_KEYWORDS = config.EXIT_KEYWORDS


# ============================================================================
# GEMINI HELPER — sends a message with optional system instruction
# ============================================================================

def call_gemini(system_instruction: str, user_message: str, history: list = None) -> str:
    """
    Call Google Gemini API.

    Args:
        system_instruction: System-level instruction for the model
        user_message: The user message / prompt
        history: Optional list of prior messages in Gemini format
                 [{"role": "user"/"model", "parts": ["text"]}]

    Returns:
        Response text string
    """
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
    """
    Convert OpenAI/Anthropic-style messages to Gemini chat history format.
    Gemini uses "user" and "model" roles (not "assistant").

    Args:
        messages: List of {"role": ..., "content": ...} dicts

    Returns:
        Gemini-compatible history list
    """
    gemini_history = []
    for msg in messages:
        role = "model" if msg["role"] == "assistant" else "user"
        gemini_history.append({
            "role": role,
            "parts": [msg["content"]]
        })
    return gemini_history


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def is_exit_command(user_input: str) -> bool:
    """Check if user input contains exit keywords"""
    user_lower = user_input.lower().strip()
    return any(keyword in user_lower for keyword in EXIT_KEYWORDS)


def extract_candidate_info(conversation_history: list) -> dict:
    """Extract structured candidate information from conversation history"""
    # Build conversation text
    conv_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])

    try:
        response_text = call_gemini(
            system_instruction="You are a data extraction assistant. Extract candidate information from conversations and return valid JSON.",
            user_message=config.CANDIDATE_INFO_EXTRACTION_PROMPT.format(conversation_text=conv_text)
        )

        # Parse JSON response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        st.warning(f"Could not extract structured data: {str(e)}")

    return {}


def generate_technical_questions(tech_stack: str) -> dict:
    """Generate technical questions based on tech stack"""
    try:
        response_text = call_gemini(
            system_instruction="You are a technical interviewer. Generate relevant technical questions and return valid JSON.",
            user_message=TECHNICAL_QUESTION_PROMPT.format(tech_stack=tech_stack)
        )

        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        st.warning(f"Error generating questions: {str(e)}")
        return {
            "questions": [
                {"id": 1, "question": f"Tell me about your experience with {tech_stack.split(',')[0].strip()}", "difficulty": "intermediate"}
            ],
            "intro": "Let's assess your technical knowledge"
        }

    return {}


def save_candidate_session(candidate_info: dict) -> str:
    """Simulate saving candidate information and return a session ID"""
    session_id = hashlib.md5(
        f"{candidate_info.get('full_name', 'unknown')}{datetime.now().isoformat()}".encode()
    ).hexdigest()[:12]

    st.session_state.candidate_sessions = st.session_state.get('candidate_sessions', {})
    st.session_state.candidate_sessions[session_id] = {
        'info': candidate_info,
        'timestamp': datetime.now().isoformat(),
        'conversation': st.session_state.messages
    }

    return session_id


def format_conversation_summary(messages: list, candidate_info: dict) -> str:
    """Format a summary of the conversation and candidate info"""
    summary = f"""
    **CANDIDATE INTERVIEW SUMMARY**
    ================================

    **Candidate Information:**
    - Name: {candidate_info.get('full_name', 'Not provided')}
    - Email: {candidate_info.get('email', 'Not provided')}
    - Phone: {candidate_info.get('phone', 'Not provided')}
    - Experience: {candidate_info.get('years_of_experience', 'Not provided')} years
    - Desired Position(s): {candidate_info.get('desired_positions', 'Not provided')}
    - Location: {candidate_info.get('current_location', 'Not provided')}
    - Tech Stack: {', '.join(candidate_info.get('tech_stack', []))}

    **Interview Duration:** {len(messages)} messages exchanged
    **Interview Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    **Next Steps:**
    1. Review candidate's technical assessment responses
    2. Schedule technical interview if qualified
    3. Contact candidate via provided communication channels
    """
    return summary


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # --- Guard: require API key before rendering anything ---
    if not config.GEMINI_API_KEY:
        st.error(
            "⚠️ **GEMINI_API_KEY is missing!**\n\n"
            "1. Go to https://aistudio.google.com/app/apikey\n"
            "2. Create a free API key\n"
            "3. Add `GEMINI_API_KEY=your_key_here` to your `.env` file\n"
            "4. Restart the app"
        )
        st.stop()

    # Initialize session state
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

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 TalentScout - Hiring Assistant</h1>
        <p>Intelligent Initial Candidate Screening for Technology Placements &nbsp;·&nbsp; Powered by Google Gemini ✨</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("### 📋 Interview Information")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Messages", len(st.session_state.messages))
        with col2:
            phase_display = {
                "greeting": "👋 Greeting",
                "info_gathering": "📝 Info Gathering",
                "technical_assessment": "🧠 Technical Assessment",
                "concluded": "✅ Concluded"
            }
            st.markdown(f"**Phase:** {phase_display.get(st.session_state.conversation_phase, 'Unknown')}")

        st.divider()

        # Extracted candidate info display
        if st.session_state.candidate_info:
            st.markdown("### ℹ️ Extracted Information")
            for key, value in st.session_state.candidate_info.items():
                if value:
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")

        st.divider()

        # Action buttons
        st.markdown("### ⚙️ Actions")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔄 Reset Chat", use_container_width=True):
                st.session_state.messages = []
                st.session_state.candidate_info = {}
                st.session_state.conversation_phase = "greeting"
                st.session_state.tech_questions_generated = False
                st.session_state.conversation_concluded = False
                st.rerun()

        with col2:
            if st.button("📥 Export", use_container_width=True):
                st.session_state.show_export = True

        st.divider()
        st.caption("🤖 Powered by **Google Gemini** (Free Tier)")
        st.caption(f"Model: `{config.MODEL}`")

    # Main chat interface
    st.markdown("### 💬 Chat Interface")

    # Display chat messages
    chat_container = st.container()

    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    # Input area
    st.divider()

    if not st.session_state.conversation_concluded:
        user_input = st.chat_input(
            "Type your response here...",
            disabled=False,
            key="user_input"
        )

        if user_input:
            # Check for exit command
            if is_exit_command(user_input):
                st.session_state.messages.append({
                    "role": "user",
                    "content": user_input
                })

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

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": conclusion_response
                })
                st.session_state.conversation_concluded = True
                st.session_state.conversation_phase = "concluded"
                st.rerun()

            # Add user message to history
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })

            # Generate response from Gemini
            try:
                with st.spinner("🤔 Processing your response..."):
                    # Build Gemini history from all previous messages (except the last user msg)
                    history = convert_to_gemini_history(st.session_state.messages[:-1])

                    assistant_message = call_gemini(
                        system_instruction=SYSTEM_PROMPT,
                        user_message=user_input,
                        history=history if history else None
                    )

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_message
                    })

                    # Extract and update candidate info periodically
                    if len(st.session_state.messages) % 6 == 0:
                        st.session_state.candidate_info = extract_candidate_info(st.session_state.messages)

                    st.rerun()

            except Exception as e:
                st.error(f"❌ Error processing request: {str(e)}")
                st.session_state.messages.pop()  # Remove the user message if there was an error

    else:
        st.markdown("""
        <div class="success-msg">
            <h4>✅ Interview Concluded</h4>
            <p>Thank you for completing the interview with TalentScout. We've saved your information and will be in touch soon!</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔄 Start New Interview"):
            st.session_state.messages = []
            st.session_state.candidate_info = {}
            st.session_state.conversation_phase = "greeting"
            st.session_state.tech_questions_generated = False
            st.session_state.conversation_concluded = False
            st.rerun()

    # Export section (if triggered)
    if st.session_state.get('show_export', False):
        st.divider()
        st.markdown("### 📊 Export Interview Data")

        candidate_info = extract_candidate_info(st.session_state.messages)
        st.session_state.candidate_info = candidate_info

        summary = format_conversation_summary(st.session_state.messages, candidate_info)
        st.markdown(summary)

        export_data = {
            "candidate_info": candidate_info,
            "conversation_messages": len(st.session_state.messages),
            "session_date": datetime.now().isoformat(),
            "interview_type": "Initial Screening",
            "messages": st.session_state.messages
        }

        st.download_button(
            label="📥 Download Interview Data (JSON)",
            data=json.dumps(export_data, indent=2),
            file_name=f"candidate_{candidate_info.get('full_name', 'unknown').replace(' ', '_')}_interview.json",
            mime="application/json"
        )

        st.download_button(
            label="📄 Download Interview Summary (MD)",
            data=summary,
            file_name=f"candidate_{candidate_info.get('full_name', 'unknown').replace(' ', '_')}_summary.md",
            mime="text/markdown"
        )


if __name__ == "__main__":
    main()