# 🎯 TalentScout — AI-Powered Hiring Assistant

> A conversational AI screening assistant built with **Streamlit** and **Google Gemini**, featuring real-time sentiment analysis, multilingual support, personalized responses, and a premium dark UI.

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?logo=streamlit)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-orange?logo=google)](https://aistudio.google.com)
[![License](https://img.shields.io/badge/License-Educational-green)](./LICENSE)

---

## 📋 Project Overview

**TalentScout** is an intelligent hiring assistant that conducts initial tech candidate screenings through a natural, human-like conversation. Powered by Google Gemini, it collects candidate information, assesses technical skills, analyzes emotional tone in real time, and supports interviews in 9 languages — all behind a premium glassmorphism dark UI.

The AI persona is **"Alex"** — a warm, experienced technical recruiter who asks questions **strictly one at a time**, holds position if a candidate skips a question, and never feels like a form.

---

## ✨ Features

### Core
| Feature | Description |
|---|---|
| 🔐 User Authentication | Secure signup & login with bcrypt password hashing (SQLite) |
| 💬 Conversational Screening | Natural multi-phase interview flow — not a form, a real conversation |
| 🎯 One-Question-at-a-Time | Strict sequential questioning — bot re-asks if candidate skips or gives vague answer |
| 📝 Smart Info Gathering | Collects name, email, phone, experience, location, role preference & tech stack |
| 🧠 Technical Assessment | 3–5 tailored questions: foundational → practical → senior trade-offs |
| 📂 Session Persistence | Saves completed interviews to SQLite per recruiter account |
| 📤 Multi-Format Export | Download as **CSV**, **JSON**, or **Markdown** report |

### Advanced
| Feature | Description |
|---|---|
| 😊 Sentiment Analysis | Detects 7 candidate emotions per message (Confident, Nervous, Excited, Confused, Enthusiastic, Frustrated, Neutral) |
| 🌐 Multilingual Support | Conduct interviews in 9 languages: English, Hindi, Spanish, French, German, Arabic, Chinese, Japanese, Portuguese |
| 🎯 Personalized Responses | AI greets returning recruiters with context from past sessions |
| 📊 Live Sentiment Dashboard | Sidebar shows dominant mood, trend (improving/declining/stable) and emotion breakdown |

### UI
| Feature | Description |
|---|---|
| 🎨 Glassmorphism Dark Theme | Full CSS design token system, animated gradient navbar, premium card layouts |
| 📈 Progress Tracker | Visual step bar: Greeting → Info → Technical → Concluded |
| ⚡ Micro-Animations | Fade-in messages, hover lifts, focus glow on chat input |
| 📊 Live Stats Cards | Message count and candidate response count in the sidebar |
| 🖼️ Candidate Avatar | Auto-generated DiceBear avatar per candidate name |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│            hiring_assistant.py  (Streamlit Frontend)        │
│  Auth gate · Navbar · Progress tracker · Chat UI            │
│  Sentiment badges · Language selector · Export panel        │
├─────────────────────────────────────────────────────────────┤
│                      features.py                            │
│  analyze_sentiment()  — per-message emotion via Gemini      │
│  get_multilingual_system_prompt()  — language injection     │
│  build_personalized_context()  — past session greeting      │
│  SUPPORTED_LANGUAGES  — 9-language registry                 │
├─────────────────────────────────────────────────────────────┤
│                       auth.py                               │
│  SQLite DB init · signup() · login() · save_session()       │
│  get_user_sessions() · bcrypt hashing                       │
├─────────────────────────────────────────────────────────────┤
│                      config.py                              │
│  SYSTEM_PROMPT (Alex persona + hold-position rules)         │
│  TECHNICAL_QUESTION_PROMPT · CANDIDATE_INFO_EXTRACTION_PROMPT│
│  CONCLUSION_TEMPLATE · CUSTOM_CSS · PAGE_CONFIG · FEATURES  │
├─────────────────────────────────────────────────────────────┤
│                  Google Gemini API                          │
│  gemini-2.5-flash (default, free tier)                      │
│  Multi-turn chat · JSON extraction · Sentiment classification│
└─────────────────────────────────────────────────────────────┘
```

### Conversation Flow

```
START
  │
  ├─→ AUTH GATE
  │    ├─→ Login  (username + password)
  │    └─→ Sign Up (username, email, password)
  │
  └─→ CHAT APP
       │
       ├─→ 👋 GREETING  — Alex introduces himself, asks for name only
       │
       ├─→ 📝 INFO GATHERING  — one field per turn (strictly)
       │    Email → Phone → Location → Experience → Role → Tech Stack
       │    (Bot re-asks if skipped or vague — never moves forward)
       │
       ├─→ 🧠 TECHNICAL ASSESSMENT  — one question per turn
       │    Foundational → Practical → Senior trade-offs
       │    (Bot re-asks with hints if "I don't know" or dodge)
       │
       └─→ ✅ CONCLUSION
            ├─→ Warm recap shown
            ├─→ Session auto-saved to SQLite
            ├─→ Sentiment summary displayed
            └─→ Export: CSV / JSON / Markdown
```

### Sentiment Analysis Flow

```
Candidate types message
       │
       ▼
analyze_sentiment(message)   ←── Gemini mini-call (10 tokens max)
       │
       ▼
Returns: { emoji, color, label }
       │
       ├─→ Badge shown inline on message bubble
       └─→ Appended to sentiment_history[]
                │
                └─→ Sidebar: dominant mood + trend + bar chart
```

---

## 💻 Technology Stack

| Component | Technology | Version |
|---|---|---|
| UI Framework | Streamlit | ≥ 1.32.0 |
| Language Model | Google Gemini 2.5 Flash | Free Tier |
| Gemini SDK | google-generativeai | ≥ 0.8.3 |
| Auth & DB | SQLite + bcrypt | Built-in / ≥ 3.2.0 |
| Env Management | python-dotenv | ≥ 1.0.0 |
| Language | Python | 3.9+ |

---

## 🚀 Installation & Setup

### Prerequisites

- Python **3.9+**
- A **free** Google Gemini API key → [Get it here](https://aistudio.google.com/app/apikey)

### Step 1 — Clone the Repository

```bash
git clone https://github.com/dnyanesh3005/TalentScout_Hiring_Assistant.git
cd TalentScout_Hiring_Assistant
```

### Step 2 — Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure Environment Variables

Copy the example file and add your API key:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Required — get your free key from https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Optional
MODEL=gemini-2.5-flash
DEBUG=false
MAX_TOKENS=1000
TEMPERATURE=0.7
```

### Step 5 — Run the App

```bash
streamlit run hiring_assistant.py
```

Open **`http://localhost:8501`** in your browser.

---

## 📖 Usage Guide

### First-Time Setup

1. Open the app → you'll see the **TalentScout** auth screen.
2. Go to **Create Account** tab → register your recruiter account.
3. Switch to **Sign In** → log in.
4. You're now inside the interview dashboard.

### Running an Interview

1. Select the **interview language** from the sidebar (default: English).
2. The candidate sends the first message — Alex greets them and starts the flow.
3. The **progress tracker** at the top shows the current phase.
4. **Sentiment badges** appear in real time on each candidate message.
5. When the candidate types an exit keyword, the session concludes and is auto-saved.

### Exit Keywords

Type any of these to gracefully end the interview:

`exit` · `quit` · `bye` · `goodbye` · `done` · `finish` · `see you` · `thanks bye` · `thank you bye`

### Sidebar Actions

| Control | Action |
|---|---|
| 🌐 Language | Switch interview language (9 options) |
| 🧠 Sentiment Panel | Live mood tracker with trend and breakdown |
| 🔄 Reset | Clear current interview and start fresh |
| 📊 Export | Open export panel (CSV / JSON / Report) |
| 🚪 Logout | Return to the auth screen |
| 📂 Past Sessions | Last 5 saved interviews for this recruiter |
| 📊 Stats | Message count and candidate response count |

### Exporting Interview Data

- **📊 CSV** — Candidate info + full chat history + sentiment labels per message
- **📦 JSON** — Structured JSON with messages, metadata, language used, and sentiment history
- **📄 Markdown** — Formatted summary report for documentation

---

## 🧠 Prompt Engineering

### The "Alex" Persona

The AI plays **Alex**, a warm and experienced technical recruiter. Key design principles:

- **One question per message, always** — strictly enforced via the system prompt
- **Hold-position logic** — if a candidate skips or gives a vague answer, Alex re-asks the same question with a hint instead of moving forward
- **Validity thresholds** — the prompt defines what counts as a valid answer per field (e.g. email must have "@", phone must have 7+ digits)
- **Adaptive tone** — more casual with juniors, peer-level with seniors
- **No robotic checklists** — info is gathered through natural conversation

### Hold-Position Examples (built into the prompt)

| Candidate Response | Alex's Action |
|---|---|
| Skips email question | Re-asks: *"I just need an email so we can follow up — like name@gmail.com?"* |
| "I work with computers" for tech stack | Probes: *"Could you be more specific? Python, JS, Java? Any frameworks?"* |
| "I don't know" to a technical question | Encourages: *"No pressure — just give me your best guess or how you'd think about it!"* |
| Goes off-topic | Acknowledges briefly, then re-asks the exact same question |

### Candidate Info Extraction

Runs every 6 messages via a dedicated Gemini call. Returns:

```json
{
  "full_name": "Priya Sharma",
  "email": "priya@example.com",
  "phone": "+91 9876543210",
  "years_of_experience": 4,
  "desired_positions": "Full Stack Developer",
  "current_location": "Pune, India",
  "remote_preference": "open to both",
  "tech_stack": ["Python", "React", "PostgreSQL", "Docker"],
  "technical_responses": ["Explained REST vs GraphQL trade-offs", "Described Docker networking"],
  "overall_impression": "Strong backend knowledge, solid communication"
}
```

---

## 📁 Project Structure

```
TalentScout_Hiring_Assistant/
├── hiring_assistant.py    # Main Streamlit app — auth gate, chat UI, all features
├── features.py            # Sentiment analysis, multilingual support, personalization
├── auth.py                # SQLite user auth (signup, login, session management)
├── config.py              # Prompts, CSS design system, page config, feature flags
├── utils.py               # Validation and utility helpers
├── gradio_app.py          # Alternative Gradio interface (optional)
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker containerization
├── setup.bat              # Windows quick-setup script
├── test_app.py            # Test suite
├── .env                   # API keys — NOT committed to git
├── .env.example           # Template for new developers
├── .gitignore             # Excludes .env, __pycache__, *.db, etc.
├── .streamlit/
│   └── config.toml        # Streamlit theme configuration
└── talentscout.db         # SQLite database (auto-created on first run)
```

---

## 🌐 Multilingual Support

TalentScout supports interviews in **9 languages**:

| Language | Flag | Native Name |
|---|---|---|
| English | 🇺🇸 | English |
| Hindi | 🇮🇳 | हिन्दी |
| Spanish | 🇪🇸 | Español |
| French | 🇫🇷 | Français |
| German | 🇩🇪 | Deutsch |
| Arabic | 🇸🇦 | العربية |
| Chinese | 🇨🇳 | 中文 |
| Japanese | 🇯🇵 | 日本語 |
| Portuguese | 🇧🇷 | Português |

The selected language is appended to the system prompt, so the entire conversation — including Alex's questions and the conclusion message — is in the chosen language.

---

## 😊 Sentiment Analysis

Each candidate message is analyzed by a fast Gemini micro-call (10 tokens) and classified into one of 7 emotional states:

| Emotion | Emoji | Color |
|---|---|---|
| Confident | 😊 | Green |
| Nervous | 😰 | Amber |
| Excited | 🤩 | Purple |
| Confused | 😕 | Red |
| Neutral | 😐 | Slate |
| Frustrated | 😤 | Orange |
| Enthusiastic | 🚀 | Cyan |

**Outputs:**
- Inline badge on each user message bubble
- Sidebar sentiment card (dominant mood + trend)
- Visual emotion breakdown bar chart
- Sentiment labels included in CSV/JSON exports

---

## 🔒 Authentication & Data Storage

### Auth Flow

1. **Signup** — `bcrypt.hashpw()` → stored in `users` table
2. **Login** — `bcrypt.checkpw()` against stored hash
3. **Session** — stored in Streamlit `session_state` (in-memory per browser tab)

### Database Schema

```sql
CREATE TABLE users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT UNIQUE NOT NULL,
    email         TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at    TEXT NOT NULL
);

CREATE TABLE sessions (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id        INTEGER NOT NULL,
    username       TEXT NOT NULL,
    session_date   TEXT NOT NULL,
    messages_count INTEGER DEFAULT 0,
    candidate_name TEXT,
    candidate_role TEXT,
    tech_stack     TEXT,
    chat_export    TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 🐳 Docker Deployment

```bash
# Build
docker build -t talentscout .

# Run
docker run -p 8501:8501 -e GEMINI_API_KEY=your_key_here talentscout
```

### Streamlit Cloud Deployment

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → set `hiring_assistant.py` as the entry point
4. Add `GEMINI_API_KEY` under **Secrets**
5. Deploy ✅

---

## 🛠️ Challenges & Solutions

| Challenge | Solution |
|---|---|
| Bot moving forward on skipped questions | System prompt hold-position logic with validity thresholds per field |
| Robotic interview feel | "Alex" persona with adaptive tone, reactions, and natural follow-ups |
| Sentiment without a dedicated API | Gemini micro-call (10 tokens max) — fast and free |
| Language switching mid-session | Language instruction appended to system prompt on every API call |
| Structured data from free-form chat | Dedicated extraction prompt → Gemini JSON → regex `{...}` parse |
| Free API rate limits | Sentiment runs per message; extraction runs every 6 messages |
| Password security | bcrypt with per-password salts — never stores plaintext |

---

## 🐛 Troubleshooting

### `GEMINI_API_KEY` not found
```bash
# Make sure .env exists with your key
echo "GEMINI_API_KEY=your_key_here" > .env
```

### Port 8501 already in use
```bash
# Windows
taskkill /f /im streamlit.exe

# Then restart
streamlit run hiring_assistant.py
```

### `ModuleNotFoundError`
```bash
pip install -r requirements.txt
```

### Quota / rate limit error from Gemini
- Wait 60 seconds and retry
- Switch to `gemini-2.0-flash` in `.env` for higher free-tier limits

### Session data not saving
- `talentscout.db` is auto-created in the project folder on first run
- Ensure the app has write permission to the directory

---

## 📈 Roadmap (Phase 3)

- [ ] **Resume Parsing** — upload PDF/DOCX and auto-fill candidate info
- [ ] **Candidate Scoring** — automatic ranking and recommendation engine
- [ ] **ATS Integration** — webhook push to Greenhouse, Lever, or Workday
- [ ] **Analytics Dashboard** — interview stats, conversion rates, avg sentiment per role
- [ ] **Voice Mode** — audio input/output for hands-free interviews

---

## 🔗 Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Gemini API Docs](https://ai.google.dev/gemini-api/docs)
- [Google AI Studio — Free API Key](https://aistudio.google.com/app/apikey)
- [bcrypt Python Docs](https://pypi.org/project/bcrypt/)

---

## 👤 Author

**Dnyaneshwar Kale**  
[GitHub](https://github.com/dnyanesh3005) · TalentScout AI Hiring Assistant

---

**Version**: 2.0.0 · **Last Updated**: May 2026 · **Status**: ✅ Production Ready