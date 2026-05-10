# 🎯 TalentScout — Intelligent Hiring Assistant Chatbot

> An AI-powered candidate screening chatbot built with **Streamlit** and **Google Gemini**, featuring user authentication, session persistence, and multi-format data export.

---

## 📋 Project Overview

**TalentScout** is an intelligent hiring assistant chatbot designed for technology recruitment agencies to conduct initial candidate screening. The application uses Google Gemini's large language model to gather candidate information, assess technical expertise, generate relevant technical questions, and persist interview sessions for future reference.

### ✨ Key Features

| Feature | Description |
|---|---|
| 🔐 User Authentication | Secure signup & login with bcrypt password hashing (SQLite backend) |
| 💬 Conversational Interview | Natural, multi-phase interview flow powered by Google Gemini |
| 📝 Auto Info Gathering | Collects name, email, phone, experience, location, desired position & tech stack |
| 🧠 Technical Assessment | Generates 3–5 tailored technical questions based on the candidate's tech stack |
| 📂 Session Persistence | Saves completed interview sessions to a local SQLite database per user |
| 📤 Multi-Format Export | Download interview data as **CSV**, **JSON**, or **Markdown** report |
| 🎨 Premium Dark UI | Custom Streamlit dark theme with Inter typography and glassmorphism-inspired styling |
| 🐳 Docker Ready | Full Dockerfile included for containerized deployment |

---

## 🏗️ Architecture & Design

### System Components

```
┌───────────────────────────────────────────────────────┐
│              Streamlit Frontend (hiring_assistant.py) │
│  - Auth gate (login / signup)                         │
│  - Top navbar, sidebar, chat UI, export panel         │
├───────────────────────────────────────────────────────┤
│               Application Logic                       │
│  - Exit command detection                             │
│  - Candidate info extraction (via Gemini)             │
│  - Conversation state management                      │
│  - CSV / JSON / Markdown export builders              │
├───────────────────────────────────────────────────────┤
│                   auth.py                             │
│  - SQLite DB init (users + sessions tables)           │
│  - signup() / login() with bcrypt hashing             │
│  - save_session() / get_user_sessions()               │
├───────────────────────────────────────────────────────┤
│                   config.py                           │
│  - All prompts, CSS, page config, feature flags       │
│  - Reads .env via python-dotenv                       │
├───────────────────────────────────────────────────────┤
│            Google Gemini API (generativeai)           │
│  - gemini-2.5-flash (default, free tier)              │
│  - Multi-turn chat history support                    │
│  - JSON-structured extraction responses               │
└───────────────────────────────────────────────────────┘
```

### Conversation Flow

```
START
  │
  ├─→ AUTH GATE
  │    ├─→ Login (username + password)
  │    └─→ Sign Up (username, email, password)
  │
  └─→ CHAT APP
       │
       ├─→ 👋 GREETING PHASE
       │    └─→ Chatbot greets candidate, explains purpose
       │
       ├─→ 📝 INFORMATION GATHERING PHASE
       │    ├─→ Full name, email, phone
       │    ├─→ Years of experience, desired position(s)
       │    ├─→ Current location
       │    └─→ Tech stack (languages, frameworks, tools)
       │
       ├─→ 🧠 TECHNICAL ASSESSMENT PHASE
       │    ├─→ 3–5 questions generated from tech stack
       │    ├─→ Progressive difficulty (beginner → advanced)
       │    └─→ Context-aware follow-up questions
       │
       └─→ ✅ CONCLUSION PHASE
            ├─→ Candidate summary displayed
            ├─→ Session auto-saved to SQLite DB
            ├─→ Next-steps information shown
            └─→ Export options (CSV / JSON / Markdown)
```

### Exit Keywords

Type any of the following to gracefully conclude an interview:

`exit` · `quit` · `bye` · `goodbye` · `done` · `finish` · `see you` · `thanks bye` · `thank you bye`

---

## 💻 Technology Stack

| Component | Technology | Version |
|---|---|---|
| UI Framework | Streamlit | ≥ 1.32.0 |
| Language Model | Google Gemini 2.5 Flash | Free Tier |
| Gemini SDK | google-generativeai | ≥ 0.8.3 |
| Auth & DB | SQLite + bcrypt | Built-in / ≥ 3.2.0 |
| Env Management | python-dotenv | ≥ 1.0.0 |
| Gradio (optional) | gradio | ≥ 5.0.0 |
| Language | Python | 3.9+ |

### Key Libraries

- **streamlit** — Web UI framework for the chat interface
- **google-generativeai** — Official Google Gemini API SDK
- **python-dotenv** — Loads `GEMINI_API_KEY` and other config from `.env`
- **bcrypt** — Secure password hashing for user auth
- **sqlite3** — Built-in Python module for local database (users + sessions)
- **json / csv / io** — Multi-format data export
- **re** — Regex-based JSON extraction from model responses

### Why Google Gemini?

- **Free tier available** — no credit card required for `gemini-2.5-flash`
- **Multi-turn chat API** — native history support via `start_chat()`
- **Strong instruction following** — reliable JSON output for data extraction
- **Configurable** — swap model via `MODEL` env var without code changes

---

## 🚀 Installation & Setup

### Prerequisites

- Python **3.9+**
- A **free** Google Gemini API key → [Get it here](https://aistudio.google.com/app/apikey)
- Git

### Step 1 — Clone the Repository

```bash
git clone <repository-url>
cd AthereAi
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

Create a `.env` file in the project root (or copy and edit the example below):

```env
# Required — get your free key from https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Optional — Model selection (free models)
# Options: gemini-2.5-flash | gemini-2.0-flash | gemini-2.5-pro
MODEL=gemini-2.5-flash

# Optional — Application Settings
DEBUG=false
MAX_TOKENS=1000
TEMPERATURE=0.7
```

### Step 5 — Run the Application

```bash
streamlit run hiring_assistant.py
```

The app will open at **`http://localhost:8501`**

---

## 📖 Usage Guide

### First-Time Setup

1. Open the app — you'll see the **TalentScout** auth screen.
2. Go to the **Sign Up** tab → create your recruiter account.
3. Switch to **Login** → enter your credentials.
4. You're now in the interview dashboard.

### Running an Interview

1. The chat area will prompt the candidate to send the first message.
2. The AI assistant guides the conversation through all four phases automatically.
3. Candidate information is extracted periodically in the background.
4. When the candidate types an **exit keyword**, the session concludes and is saved.

### Sidebar Actions

| Button | Action |
|---|---|
| 🔄 Reset Chat | Clear current interview and start fresh |
| 📥 Export | Open the export panel (CSV / JSON / Report) |
| 📄 View Report | Show and download the interview summary |
| 🚪 Logout | Clear session and return to the auth screen |
| 📂 Past Sessions | Shows the last 5 saved interviews for the logged-in user |

### Exporting Interview Data

After an interview concludes (or via the Export button):

- **📊 CSV** — Candidate info + full chat history in spreadsheet format
- **📦 JSON** — Structured JSON with all messages and metadata
- **📄 Markdown Report** — Formatted summary suitable for documentation

---

## 🧠 Prompt Engineering

### System Prompt Design

The `SYSTEM_PROMPT` in `config.py` structures the entire interview:

```
Role Definition → Conversation Phases → Behavioral Guidelines → Exit Handling
```

Key design decisions:
- **One or two questions at a time** — avoids overwhelming the candidate
- **Contextual follow-ups** — uses full message history passed as `history=`
- **Fallback handling** — redirects off-topic inputs back to the interview
- **Professional yet friendly tone** — makes candidates comfortable

### Candidate Info Extraction

A dedicated `CANDIDATE_INFO_EXTRACTION_PROMPT` is sent to Gemini every 6 messages. It returns a JSON object with:

```json
{
  "full_name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "+1234567890",
  "years_of_experience": "5",
  "desired_positions": "Backend Engineer",
  "current_location": "Pune, India",
  "tech_stack": ["Python", "Django", "PostgreSQL", "Docker"]
}
```

### Technical Question Generation

The `TECHNICAL_QUESTION_PROMPT` takes the extracted `tech_stack` and returns:

```json
{
  "questions": [
    {"id": 1, "question": "...", "difficulty": "beginner"},
    {"id": 2, "question": "...", "difficulty": "intermediate"},
    {"id": 3, "question": "...", "difficulty": "advanced"}
  ],
  "intro": "Let's assess your Python and Django expertise..."
}
```

---

## 📁 Project Structure

```
AthereAi/
├── hiring_assistant.py   # Main Streamlit app (auth gate + chat UI)
├── auth.py               # SQLite user auth (signup, login, sessions)
├── config.py             # All constants: prompts, CSS, page config
├── utils.py              # Utility helpers
├── gradio_app.py         # Alternative Gradio interface (optional)
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker containerization
├── setup.bat             # Windows quick-setup script
├── talentscout.db        # SQLite database (auto-created on first run)
├── .env                  # API key and config (not committed to git)
├── .streamlit/
│   └── config.toml       # Streamlit theme configuration
└── test_app.py           # Test suite
```

---

## 🔒 Authentication & Data Storage

### Auth Flow

1. **Signup** — username + email + password → `bcrypt.hashpw()` → stored in `users` table
2. **Login** — username + password → `bcrypt.checkpw()` against stored hash
3. **Session** — stored in Streamlit `session_state` (in-memory per browser tab)

### Database Schema (SQLite — `talentscout.db`)

```sql
-- Users table
CREATE TABLE users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT UNIQUE NOT NULL,
    email         TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at    TEXT NOT NULL
);

-- Sessions table
CREATE TABLE sessions (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id        INTEGER NOT NULL,
    username       TEXT NOT NULL,
    session_date   TEXT NOT NULL,
    messages_count INTEGER DEFAULT 0,
    candidate_name TEXT,
    candidate_role TEXT,
    tech_stack     TEXT,
    chat_export    TEXT,   -- Full JSON of all messages
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 🐳 Docker Deployment

### Build & Run with Docker

```bash
# Build the image
docker build -t talentscout .

# Run the container (pass your Gemini API key)
docker run -p 8501:8501 -e GEMINI_API_KEY=your_key_here talentscout
```

Access the app at **`http://localhost:8501`**

### Streamlit Cloud Deployment

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and set `hiring_assistant.py` as the entry point
4. Add `GEMINI_API_KEY` under **Secrets** in the app settings
5. Deploy — the app auto-deploys on every push

---

## 🛠️ Challenges & Solutions

| Challenge | Solution |
|---|---|
| Structured data from free-form chat | Dedicated extraction prompt → Gemini JSON output → regex `{...}` parse |
| Context across many messages | Full `history=` list passed to `model.start_chat()` on every call |
| Off-topic / irrelevant input | System prompt fallback instructs AI to redirect politely |
| Free API rate limits | Extraction runs every 6 messages, not on every turn |
| Password security | `bcrypt` with per-password salts — never stores plaintext |
| Session data persistence | SQLite `sessions` table saves full chat JSON on conclusion |

---

## 📈 Future Enhancements (Phase 2)

Planned features (already flagged in `config.py` under `FEATURES`):

- [ ] **Sentiment Analysis** — gauge candidate confidence in real time
- [ ] **Multilingual Support** — interviews in multiple languages
- [ ] **Resume Parsing** — upload PDF and auto-fill candidate info
- [ ] **Candidate Scoring** — automatic ranking and recommendation
- [ ] **ATS Integration** — webhook push to external applicant tracking systems
- [ ] **Analytics Dashboard** — interview stats, conversion rates, time-to-hire

---

## 🐛 Troubleshooting

### `GEMINI_API_KEY` not found
Ensure `.env` exists in the project root and contains:
```
GEMINI_API_KEY=your_key_here
```
Then restart the app.

### `ModuleNotFoundError` for any package
```bash
pip install -r requirements.txt
```

### Quota / rate limit error from Gemini
- The free tier has per-minute request limits.
- Wait 60 seconds and retry.
- Alternatively, switch to `gemini-2.0-flash` which has higher free-tier limits.

### Session data not saving
- `talentscout.db` is created automatically on first run in the project directory.
- Ensure the app has write permission to the project folder.

### App crashes on login
- Run `python auth.py` once to verify the database initialises correctly.
- Delete `talentscout.db` and restart to reset all users.

---

## 📝 Code Quality

- ✅ Modular separation: `hiring_assistant.py` / `auth.py` / `config.py`
- ✅ All prompts centralised in `config.py` — no hard-coded strings in logic
- ✅ bcrypt password hashing with salt
- ✅ SQLite parameterised queries (no SQL injection)
- ✅ Graceful error handling with user-friendly Streamlit messages
- ✅ Session state properly initialised before use
- ✅ CSV / JSON export with structured field mapping

---

## 🔗 Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Gemini API Docs](https://ai.google.dev/gemini-api/docs)
- [Google AI Studio (free API key)](https://aistudio.google.com/app/apikey)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [bcrypt Python Docs](https://pypi.org/project/bcrypt/)
- [SQLite Python Docs](https://docs.python.org/3/library/sqlite3.html)

---

## 📄 License

This project is provided for educational and evaluation purposes.

---

## 👤 Author

**Dnyaneshwar Kale**  
Developed as part of a TalentScout AI Hiring Assistant project.

---

**Last Updated**: May 2026 · **Version**: 2.0.0 · **Status**: ✅ Production Ready