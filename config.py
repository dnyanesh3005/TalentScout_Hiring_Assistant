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

SYSTEM_PROMPT = """You are Alex, a warm and experienced Technical Recruiter at TalentScout — a modern tech recruitment agency. You conduct initial candidate screening conversations.

## Your Personality
- Friendly, encouraging, and genuinely curious about the candidate
- Conversational — you sound like a real person, NOT a form or a checklist
- You celebrate small wins (e.g., "That's great experience!", "Impressive stack!")
- You adapt your tone: more casual with junior candidates, more peer-level with seniors

---

## CRITICAL RULE — ONE QUESTION, HOLD POSITION
You ask exactly **ONE question per message**. You do **NOT** move to the next question or topic until the current question is properly answered.

### What counts as a valid answer:
- **Name** → Any name given (even just a first name)
- **Email** → Must have "@" and a domain (e.g. name@gmail.com)
- **Phone** → Any 7+ digit number
- **Experience** → A number or rough range ("3 years", "about 2", "5+")
- **Desired role** → Any title or description of what they want
- **Location** → Any city, country, or the word "remote"
- **Tech stack** → At least one specific technology named
- **Technical question** → Any genuine attempt — even a partial answer counts

### If the answer is missing, vague, off-topic, or "I don't know":
1. Do NOT move to the next question — stay on the current one
2. Warmly acknowledge what they said
3. Re-ask the EXACT same question in a friendlier, simpler way
4. Add a short hint or example to guide them
5. Only proceed once you receive a valid answer

### Hold-position examples:

Candidate skips email → Alex: "No problem! I just need an email so our team can follow up — something like name@gmail.com works great. What's yours?"

Candidate says "I work with computers" for tech stack → Alex: "Nice! Could you be more specific? For example — do you use Python, JavaScript, or Java? Any frameworks like React or Django, or databases like MySQL or MongoDB?"

Candidate says "some years" for experience → Alex: "Got it, roughly how many though — even a ballpark like '2-3 years' helps me a lot!"

Candidate says "I don't know" / "pass" to a technical question → Alex: "No pressure at all! Just give me your best guess or how you'd think about it — there's really no wrong answer here."

Candidate goes off-topic → Alex: Briefly acknowledge, then: "That's interesting! Coming back to my earlier question though — [re-ask the exact same question]"

## Conversation Flow

### Step 1 — Warm Opening (first message only)
- Introduce yourself as Alex from TalentScout
- Say this is a relaxed 10-15 min screening, no pressure at all
- Ask ONLY for their name — nothing else in this first message

### Step 2 — Information Gathering (strictly one field per turn, in this order)
1. Email address
2. Phone number
3. Current location + remote or on-site preference
4. Years of experience in tech
5. What kind of role they're looking for
6. Tech stack — "walk me through what you work with day-to-day"

Rules:
- ONE field per message — no bundling
- Acknowledge each answer warmly before asking the next
- If the answer is incomplete or skipped, re-ask it — never skip ahead
- If they seem nervous or hesitant, reassure them it's just a casual chat

### Step 3 — Technical Deep-Dive (strictly one question per turn)
- Ask ONE technical question, then wait for the response
- If the answer is blank, "I don't know", or a clear dodge: re-ask with a simpler framing or a hint — do NOT skip it
- If the answer is partial: ask a targeted follow-up on THAT question before moving on
- Only move to the next question once the current one is meaningfully answered
- Ask 3-5 questions total, progressing: foundational → practical → senior trade-offs

### Step 4 — Wrap-Up
- Briefly summarise what you heard about the candidate (shows you listened)
- Explain next steps clearly
- Ask if they have any questions for you
- End warmly

## Hard Rules
- **NEVER ask more than 1 question per message — no exceptions**
- **NEVER move to the next question if the current one wasn't answered**
- **NEVER skip a field just because the candidate ignored it — re-ask it**
- NEVER repeat information the candidate already gave
- NEVER say "As an AI" or break character
- If off-topic: briefly acknowledge, then re-ask the exact same question
- Keep responses concise — 2-4 sentences per turn
- Use the candidate's name occasionally to keep it personal"""

TECHNICAL_QUESTION_PROMPT = """The candidate's tech stack is: {tech_stack}

Generate 3-5 conversational technical questions for a job interview screening. Each question should:
1. Sound like something a real senior engineer would ask over coffee — NOT a quiz
2. Progress from fundamentals → practical → senior-level trade-offs
3. Be specific to the technologies listed (not generic)
4. Be open-ended enough to reveal depth of knowledge
5. Have a natural follow-up angle if the first answer is shallow

Avoid:
- Trick questions or trivia
- Questions answerable with a simple yes/no
- Overly academic/textbook questions

Return as valid JSON:
{{
    "intro": "A casual 1-sentence bridge into the technical section (e.g., 'Great, let me ask you a few things about your stack.')",
    "questions": [
        {{"id": 1, "question": "...", "difficulty": "foundational", "follow_up": "..."}},
        {{"id": 2, "question": "...", "difficulty": "practical", "follow_up": "..."}},
        {{"id": 3, "question": "...", "difficulty": "advanced", "follow_up": "..."}}
    ]
}}"""

CANDIDATE_INFO_EXTRACTION_PROMPT = """Extract candidate information from the conversation below. Be smart about inference:
- If the candidate says "I'm in Pune" that's their current_location
- If they mention "5+ years" that's years_of_experience = 5
- tech_stack should be a clean list of distinct technologies (e.g. ["Python", "React", "PostgreSQL"])
- technical_responses should capture their answers to technical questions as short summaries
- desired_positions should reflect what they said they're looking for (not just a job code)

Return ONLY valid JSON, no explanation. Use null for any field not mentioned.

Schema:
{{
  "full_name": string | null,
  "email": string | null,
  "phone": string | null,
  "years_of_experience": number | null,
  "desired_positions": string | null,
  "current_location": string | null,
  "remote_preference": string | null,
  "tech_stack": list[string] | null,
  "technical_responses": list[string] | null,
  "overall_impression": string | null
}}

Conversation:
{conversation_text}"""

# ============================================================================
# MESSAGE TEMPLATES
# ============================================================================

CONCLUSION_TEMPLATE = """It was really great chatting with you, {name}! 🙌

Based on our conversation, here's a quick recap of what I've noted:

- 🧑‍💻 **Role you're targeting:** {position}
- ⏳ **Experience:** {experience} years
- 🛠 **Tech Stack:** {tech_stack}

**What happens next?**
Our recruiting team will review your profile over the next **1–2 business days**. If there's a strong match with our current openings, we'll reach out to you at **{email}** (or **{phone}**) to schedule a deeper technical conversation.

A couple of things to keep in mind:
- You don't need to do anything right now — we'll reach out
- If you have questions in the meantime, drop us a note at **careers@talentscout.com**
- Feel free to check our open roles at **www.talentscout.com**

Thanks again for your time — you've got a solid background and we look forward to exploring opportunities together. Best of luck! 🚀"""

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
    /* ── Google Fonts ─────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    /* ── CSS Variables / Design Tokens ───────────────── */
    :root {
        --bg-base:       #0d0f1a;
        --bg-surface:    #13151f;
        --bg-card:       #1a1d2e;
        --bg-elevated:   #1f2236;
        --border:        #252840;
        --border-light:  #2e3250;
        --accent:        #6366f1;
        --accent-2:      #8b5cf6;
        --accent-glow:   rgba(99,102,241,0.25);
        --text-primary:  #e2e8f0;
        --text-secondary:#94a3b8;
        --text-muted:    #475569;
        --success:       #10b981;
        --warning:       #f59e0b;
        --danger:        #ef4444;
        --radius-sm:     8px;
        --radius-md:     12px;
        --radius-lg:     20px;
        --radius-xl:     28px;
        --shadow-glow:   0 0 40px rgba(99,102,241,0.15);
    }

    /* ── Reset & Base ─────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'Inter', 'Space Grotesk', sans-serif;
        background-color: var(--bg-base) !important;
        color: var(--text-primary);
    }
    header[data-testid="stHeader"] { display: none; }
    .block-container {
        padding-top: 0.5rem !important;
        max-width: 100% !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }

    /* ── Animated Gradient Background ────────────────── */
    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp {
        background: linear-gradient(135deg, #0d0f1a 0%, #111328 40%, #0f1123 70%, #0d0f1a 100%) !important;
    }

    /* ── Top Navbar (Glassmorphism) ───────────────────── */
    .top-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(26,29,46,0.80);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        padding: 14px 28px;
        border-radius: var(--radius-md);
        margin-bottom: 20px;
        border: 1px solid var(--border-light);
        box-shadow: var(--shadow-glow);
        position: relative;
        overflow: hidden;
    }
    .top-navbar::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent), var(--accent-2), #ec4899, var(--accent));
        background-size: 200% 100%;
        animation: gradientShift 4s ease infinite;
    }
    .top-navbar .logo {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-primary);
        display: flex;
        align-items: center;
        gap: 10px;
        letter-spacing: -0.3px;
    }
    .logo-icon {
        background: linear-gradient(135deg, var(--accent), var(--accent-2));
        border-radius: 8px;
        padding: 6px 8px;
        font-size: 1rem;
        box-shadow: 0 0 16px var(--accent-glow);
    }
    .nav-badge {
        background: rgba(99,102,241,0.15);
        border: 1px solid rgba(99,102,241,0.3);
        color: #a5b4fc;
        font-size: 0.75rem;
        font-weight: 500;
        padding: 3px 10px;
        border-radius: 20px;
        letter-spacing: 0.3px;
    }

    /* ── Sidebar ──────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: var(--bg-surface) !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--text-secondary);
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 1rem;
    }

    /* ── Sidebar Phase Items ──────────────────────────── */
    .sidebar-phase {
        padding: 8px 14px;
        border-radius: var(--radius-sm);
        margin-bottom: 4px;
        font-size: 0.85rem;
        color: var(--text-secondary);
        border: 1px solid transparent;
        transition: all 0.2s ease;
    }
    .sidebar-phase:hover {
        background: var(--bg-card);
        border-color: var(--border);
        color: var(--text-primary);
    }

    /* ── Sentiment Badge ──────────────────────────────── */
    .sentiment-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        font-size: 0.72rem;
        font-weight: 500;
        padding: 2px 9px;
        border-radius: 20px;
        margin-left: 8px;
        opacity: 0.85;
        vertical-align: middle;
    }
    .sentiment-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 14px 16px;
        margin-bottom: 12px;
        text-align: center;
    }
    .sentiment-card .big-emoji {
        font-size: 2rem;
        display: block;
        margin-bottom: 4px;
    }
    .sentiment-card .sent-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    .sentiment-card .sent-sub {
        font-size: 0.75rem;
        color: var(--text-secondary);
        margin-top: 2px;
    }

    /* ── Progress Tracker ─────────────────────────────── */
    .progress-tracker {
        display: flex;
        align-items: center;
        gap: 0;
        margin-bottom: 18px;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 10px 20px;
        overflow-x: auto;
    }
    .progress-step {
        display: flex;
        align-items: center;
        gap: 8px;
        flex: 1;
        min-width: 0;
    }
    .step-dot {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 700;
        flex-shrink: 0;
        transition: all 0.3s ease;
    }
    .step-dot.active {
        background: linear-gradient(135deg, var(--accent), var(--accent-2));
        box-shadow: 0 0 14px var(--accent-glow);
        color: white;
    }
    .step-dot.done {
        background: var(--success);
        color: white;
    }
    .step-dot.pending {
        background: var(--bg-elevated);
        border: 1px solid var(--border-light);
        color: var(--text-muted);
    }
    .step-label {
        font-size: 0.78rem;
        font-weight: 500;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .step-label.active  { color: #a5b4fc; }
    .step-label.done    { color: var(--success); }
    .step-label.pending { color: var(--text-muted); }
    .step-connector {
        flex: 0 0 24px;
        height: 1px;
        background: var(--border-light);
        margin: 0 4px;
    }

    /* ── Session Header ───────────────────────────────── */
    .session-header {
        display: flex;
        align-items: center;
        gap: 14px;
        flex-wrap: wrap;
        background: var(--bg-card);
        padding: 14px 22px;
        border-radius: var(--radius-md) var(--radius-md) 0 0;
        border: 1px solid var(--border);
        border-bottom: 1px solid rgba(37,40,64,0.6);
    }
    .session-header h3 {
        margin: 0;
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-secondary);
    }
    .candidate-badge {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .candidate-badge img {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        border: 2px solid var(--accent);
    }
    .cand-info { display: flex; flex-direction: column; }
    .cand-name { font-size: 0.95rem; font-weight: 700; color: var(--text-primary); }
    .cand-role { font-size: 0.75rem; color: var(--text-secondary); }

    /* ── Chat Messages ────────────────────────────────── */
    div[data-testid="stChatMessage"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 14px 18px;
        margin-bottom: 14px;
        color: var(--text-primary);
        transition: border-color 0.2s ease;
        animation: fadeInUp 0.3s ease;
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: var(--bg-elevated);
        border-color: var(--border-light);
        border-left: 3px solid var(--accent);
    }
    div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        border-left: 3px solid var(--accent-2);
    }

    /* ── Chat Input ───────────────────────────────────── */
    [data-testid="stChatInput"] {
        background: var(--bg-card) !important;
        border-radius: 28px !important;
        border: 1px solid var(--border-light) !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px var(--accent-glow) !important;
    }

    /* ── Buttons ──────────────────────────────────────── */
    .stButton > button {
        background: var(--bg-elevated);
        color: var(--text-primary);
        border: 1px solid var(--border-light);
        border-radius: var(--radius-sm);
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        border-color: var(--accent);
        color: #a5b4fc;
        box-shadow: 0 0 12px var(--accent-glow);
        transform: translateY(-1px);
    }
    .stButton > button:active { transform: translateY(0); }

    /* ── Primary CTA Button ───────────────────────────── */
    .btn-primary > button {
        background: linear-gradient(135deg, var(--accent), var(--accent-2)) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px var(--accent-glow) !important;
    }
    .btn-primary > button:hover {
        box-shadow: 0 6px 20px rgba(99,102,241,0.4) !important;
        transform: translateY(-2px) !important;
    }

    /* ── Language Selector ────────────────────────────── */
    .lang-selector {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 12px 16px;
        margin-bottom: 12px;
    }
    .lang-selector label { font-size: 0.8rem; color: var(--text-secondary); }

    /* ── Tabs ─────────────────────────────────────────── */
    button[data-baseweb="tab"] {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: var(--text-primary) !important;
        border-bottom-color: var(--accent) !important;
    }

    /* ── Forms & Inputs ───────────────────────────────── */
    [data-testid="stTextInput"] input,
    [data-testid="stTextInput"] input:focus {
        background: var(--bg-elevated) !important;
        border-color: var(--border-light) !important;
        color: var(--text-primary) !important;
        border-radius: var(--radius-sm) !important;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px var(--accent-glow) !important;
    }

    /* ── Selectbox ────────────────────────────────────── */
    [data-testid="stSelectbox"] > div > div {
        background: var(--bg-elevated) !important;
        border-color: var(--border-light) !important;
        color: var(--text-primary) !important;
        border-radius: var(--radius-sm) !important;
    }

    /* ── Success Message ──────────────────────────────── */
    .success-msg {
        background: linear-gradient(135deg, rgba(16,185,129,0.1), rgba(16,185,129,0.05));
        padding: 24px;
        border-radius: var(--radius-lg);
        border: 1px solid rgba(16,185,129,0.3);
        color: #a7f3d0;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 0 30px rgba(16,185,129,0.1);
    }
    .success-msg h4 { margin-top: 0; color: var(--success); font-size: 1.4rem; }

    /* ── Stats Cards ──────────────────────────────────── */
    .stat-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 14px;
        text-align: center;
        transition: border-color 0.2s ease, transform 0.2s ease;
    }
    .stat-card:hover {
        border-color: var(--accent);
        transform: translateY(-2px);
    }
    .stat-card .stat-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
    }
    .stat-card .stat-label {
        font-size: 0.75rem;
        color: var(--text-secondary);
        margin-top: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* ── Divider ──────────────────────────────────────── */
    hr { border-color: var(--border) !important; }

    /* ── Auth Page Card ───────────────────────────────── */
    .auth-card {
        max-width: 480px;
        margin: 0 auto;
        background: var(--bg-card);
        border: 1px solid var(--border-light);
        border-radius: var(--radius-xl);
        padding: 36px;
        box-shadow: 0 24px 80px rgba(0,0,0,0.4), var(--shadow-glow);
    }
    .auth-hero {
        text-align: center;
        margin-bottom: 28px;
    }
    .auth-hero .hero-icon {
        font-size: 3rem;
        display: block;
        margin-bottom: 12px;
        filter: drop-shadow(0 0 20px rgba(99,102,241,0.5));
    }
    .auth-hero h1 {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #e2e8f0, #a5b4fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 6px;
    }
    .auth-hero p {
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin: 0;
    }

    /* ── Scrollbar ────────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-base); }
    ::-webkit-scrollbar-thumb {
        background: var(--border-light);
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent); }

    /* ── Metric override ──────────────────────────────── */
    [data-testid="stMetric"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 12px 16px;
    }
    [data-testid="stMetricLabel"] { color: var(--text-secondary) !important; font-size: 0.8rem !important; }
    [data-testid="stMetricValue"] { color: var(--text-primary) !important; }
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
    "sentiment_analysis": True,   # ✅ Live sentiment per message
    "multilingual_support": True,  # ✅ Multi-language conversations
    "resume_parsing": False,       # TODO: Implement in Phase 3
    "candidate_scoring": False,    # TODO: Implement in Phase 3
    "ats_integration": False,      # TODO: Implement in Phase 3
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