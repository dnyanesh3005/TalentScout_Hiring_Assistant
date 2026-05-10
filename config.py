"""
Configuration and Constants for TalentScout Hiring Assistant
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================================================
# API CONFIGURATION  (Google Gemini - Free Tier)
# ============================================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
# Free models: gemini-2.5-flash (latest), gemini-2.0-flash (fast), gemini-2.5-pro (powerful)
MODEL = os.getenv("MODEL", "gemini-2.5-flash")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1000"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# ============================================================================
# CONVERSATION CONFIGURATION
# ============================================================================

CONVERSATION_PHASES = {
    "greeting": "👋 Greeting",
    "info_gathering": "📝 Information Gathering",
    "technical_assessment": "🧠 Technical Assessment",
    "concluded": "✅ Concluded"
}

EXIT_KEYWORDS = [
    "exit", "quit", "bye", "goodbye", 
    "end conversation", "done", "finish", 
    "see you", "thanks bye", "thank you bye"
]

# ============================================================================
# CANDIDATE INFORMATION FIELDS
# ============================================================================

REQUIRED_CANDIDATE_FIELDS = [
    "full_name",
    "email",
    "phone",
    "years_of_experience",
    "desired_positions",
    "current_location",
    "tech_stack"
]

# ============================================================================
# STREAMLIT UI CONFIGURATION
# ============================================================================

PAGE_CONFIG = {
    "page_title": "TalentScout - Hiring Assistant",
    "page_icon": "🤖",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# ============================================================================
# SYSTEM PROMPTS
# ============================================================================

SYSTEM_PROMPT = """You are TalentScout, an intelligent Hiring Assistant chatbot for a technology recruitment agency.

Your role is to conduct initial candidate screening through a structured conversation. You should:

1. **Greeting Phase**: Start by greeting the candidate warmly and explaining your purpose
2. **Information Gathering Phase**: Collect the following information in a conversational manner:
   - Full Name
   - Email Address
   - Phone Number
   - Years of Experience
   - Desired Position(s)
   - Current Location
   - Tech Stack (programming languages, frameworks, databases, tools)

3. **Technical Assessment Phase**: Based on their tech stack, generate 3-5 tailored technical questions

4. **Context Maintenance**: Remember all previously shared information and use it in follow-up questions

5. **Fallback Handling**: If the user provides irrelevant input, politely redirect them back to the conversation

6. **Exit Handling**: If the user says keywords like "exit", "quit", "bye", "goodbye", "end", politely conclude the conversation

Guidelines:
- Be professional yet friendly
- Ask one or two questions at a time, not all at once
- Validate information before moving forward
- If a candidate is unclear about their tech stack, provide examples
- Make technical questions progressively challenging
- Provide encouraging feedback
- Always maintain context from previous messages

Current conversation stage will be tracked, and you should know what information is still needed."""

TECHNICAL_QUESTION_PROMPT = """Based on the candidate's tech stack: {tech_stack}

Generate 3-5 technical questions that:
1. Are relevant to their specified technologies
2. Progressively increase in difficulty
3. Assess both theoretical knowledge and practical experience
4. Can be asked in a conversational manner
5. Include follow-up questions if needed

Format the response as a JSON object with this structure:
{{
    "questions": [
        {{"id": 1, "question": "...", "difficulty": "beginner/intermediate/advanced"}},
        ...
    ],
    "intro": "A brief intro about the technical assessment"
}}

Ensure valid JSON format."""

CANDIDATE_INFO_EXTRACTION_PROMPT = """Based on the conversation history provided, extract the following candidate information:
    - full_name
    - email
    - phone
    - years_of_experience
    - desired_positions
    - current_location
    - tech_stack (list)
    - technical_responses (list)
    
Return as JSON. For missing fields, use null.

Conversation:
{conversation_text}"""

# ============================================================================
# MESSAGE TEMPLATES
# ============================================================================

CONCLUSION_TEMPLATE = """Thank you for taking the time to interview with TalentScout! 

We've gathered valuable information about your background and technical expertise. Here's what we've collected:

**Summary:**
- **Name:** {name}
- **Experience:** {experience} years
- **Tech Stack:** {tech_stack}
- **Desired Position:** {position}

**Next Steps:**
1. Our team will review your responses within 24-48 hours
2. If your profile matches our current opportunities, we'll contact you via {email} or {phone}
3. You may be invited for a technical assessment or in-depth interview

**Contact Us:**
- Email: careers@talentscout.com
- Phone: +1-800-TALENT-SCOUT
- Website: www.talentscout.com

Best of luck, and we hope to hear from you soon! 🚀"""

INTERVIEW_SUMMARY_TEMPLATE = """
**CANDIDATE INTERVIEW SUMMARY**
================================

**Candidate Information:**
- Name: {full_name}
- Email: {email}
- Phone: {phone}
- Experience: {years_of_experience} years
- Desired Position(s): {desired_positions}
- Location: {current_location}
- Tech Stack: {tech_stack}

**Interview Duration:** {message_count} messages exchanged
**Interview Date:** {interview_date}

**Next Steps:**
1. Review candidate's technical assessment responses
2. Schedule technical interview if qualified
3. Contact candidate via provided communication channels
"""

# ============================================================================
# CSS STYLING
# ============================================================================

CUSTOM_CSS = """
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
    .candidate-info {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .success-msg {
        background-color: #d4edda;
        padding: 12px;
        border-radius: 6px;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .warning-msg {
        background-color: #fff3cd;
        padding: 12px;
        border-radius: 6px;
        border: 1px solid #ffeeba;
        color: #856404;
    }
</style>
"""

# ============================================================================
# ERROR MESSAGES
# ============================================================================

ERROR_MESSAGES = {
    "api_key_missing": "⚠️ GEMINI_API_KEY not found. Please set it in .env file. Get a free key at https://aistudio.google.com/",
    "api_error": "❌ Error communicating with API: {error}",
    "extraction_error": "⚠️ Could not extract structured data: {error}",
    "json_parse_error": "❌ Failed to parse JSON response: {error}",
    "invalid_input": "⚠️ Invalid input. Please try again.",
}

# ============================================================================
# SUCCESS MESSAGES
# ============================================================================

SUCCESS_MESSAGES = {
    "interview_started": "✅ Interview session started successfully!",
    "info_extracted": "✅ Candidate information extracted and updated",
    "interview_concluded": "✅ Interview concluded successfully",
    "data_exported": "✅ Interview data exported successfully",
}

# ============================================================================
# DATA VALIDATION
# ============================================================================

VALIDATION_RULES = {
    "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    "phone": r"^\+?1?\d{9,15}$",
    "years_of_experience": {"min": 0, "max": 70},
    "name_length": {"min": 2, "max": 100},
}

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO" if not DEBUG else "DEBUG"

# ============================================================================
# SESSION CONFIGURATION
# ============================================================================

SESSION_TIMEOUT_MINUTES = 60
MAX_MESSAGES_PER_SESSION = 1000
EXTRACTION_FREQUENCY = 6  # Extract candidate info every N messages

# ============================================================================
# EXPORT CONFIGURATION
# ============================================================================

EXPORT_FORMATS = ["json", "markdown"]
MAX_EXPORT_SIZE_MB = 10

# ============================================================================
# FEATURE FLAGS
# ============================================================================

FEATURES = {
    "sentiment_analysis": False,  # TODO: Implement in Phase 2
    "multilingual_support": False,  # TODO: Implement in Phase 2
    "resume_parsing": False,  # TODO: Implement in Phase 2
    "candidate_scoring": False,  # TODO: Implement in Phase 2
    "ats_integration": False,  # TODO: Implement in Phase 2
}

# ============================================================================
# VALIDATION
# ============================================================================

def validate_configuration():
    """Validate that all required configuration is present"""
    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY not found. Please set it in .env file. "
            "Get your FREE key from https://aistudio.google.com/app/apikey"
        )
    return True