# TalentScout - Intelligent Hiring Assistant Chatbot

## 📋 Project Overview

**TalentScout** is an intelligent hiring assistant chatbot designed for technology recruitment agencies to conduct initial candidate screening. The application uses advanced language models to gather candidate information, assess technical expertise, and generate relevant technical questions based on a candidate's tech stack.

### Key Features:
- **Conversational Interview**: Natural, flowing conversation that feels like talking to a recruiter
- **Automated Information Gathering**: Collects candidate details (name, email, phone, experience, location, desired positions)
- **Tech Stack Assessment**: Identifies candidate's technology proficiency areas
- **Intelligent Question Generation**: Creates 3-5 tailored technical questions based on declared tech stack
- **Context Management**: Maintains conversation context throughout the interview
- **Exit Handling**: Gracefully concludes conversations when requested
- **Data Export**: Export interview data in JSON and Markdown formats
- **Professional UI**: Clean, intuitive Streamlit interface

---

## 🎯 Purpose of Prompting

The application leverages advanced prompt engineering to:

1. **Guide Information Gathering**: Structured prompts ensure all essential candidate details are collected conversationally
2. **Generate Technical Questions**: Dynamic prompts create relevant questions matched to the candidate's tech stack
3. **Maintain Context**: System prompts enable the model to remember previous information and provide coherent follow-up questions
4. **Professional Tone**: Carefully crafted prompts ensure professional yet friendly communication
5. **Fallback Handling**: Prompts guide the model to redirect irrelevant inputs back to the interview flow

### Prompt Engineering Strategy:

**System Prompt**: Defines the role, responsibilities, and behavior guidelines for the chatbot
- Sets conversation phases (greeting → info gathering → technical assessment → conclusion)
- Specifies information to collect
- Establishes professional guidelines
- Defines exit handling behavior

**Technical Question Prompt**: Generates contextually relevant technical questions
- Takes tech stack as input
- Generates questions of progressive difficulty
- Returns structured JSON format
- Includes brief introduction to technical assessment

---

## 🏗️ Architecture & Design

### System Components:

```
┌─────────────────────────────────────────────────────┐
│           Streamlit Frontend Interface              │
├─────────────────────────────────────────────────────┤
│  - Chat Display                                     │
│  - User Input Field                                 │
│  - Sidebar with Interview Tracking                  │
│  - Export Functionality                             │
├─────────────────────────────────────────────────────┤
│        Application Logic & Message Handler          │
├─────────────────────────────────────────────────────┤
│  - Exit Command Detection                           │
│  - Candidate Info Extraction                        │
│  - Technical Question Generation                    │
│  - Conversation State Management                    │
├─────────────────────────────────────────────────────┤
│           Claude API (Anthropic)                    │
├─────────────────────────────────────────────────────┤
│  - Message Processing                              │
│  - Prompt Execution                                │
│  - Context-Aware Responses                         │
└─────────────────────────────────────────────────────┘
```

### Conversation Flow:

```
START
  │
  ├─→ GREETING PHASE
  │    └─→ Chatbot greets candidate and explains purpose
  │
  ├─→ INFORMATION GATHERING PHASE
  │    ├─→ Collects: Name, Email, Phone, Experience, Location
  │    ├─→ Collects: Desired Positions, Tech Stack
  │    └─→ Validates information conversationally
  │
  ├─→ TECHNICAL ASSESSMENT PHASE
  │    ├─→ Generates 3-5 questions based on tech stack
  │    ├─→ Asks follow-up questions based on answers
  │    └─→ Maintains context of previous responses
  │
  └─→ CONCLUSION PHASE
       ├─→ Summarizes collected information
       ├─→ Explains next steps
       ├─→ Provides contact information
       └─→ END
```

### Exit Keywords Detection:
The application monitors for conversation-ending keywords:
- "exit", "quit", "bye", "goodbye", "end", "done", "finish", "see you"

When detected, the chatbot gracefully concludes the interview and displays a summary.

---

## 💻 Technical Details

### Technology Stack:

| Component | Technology | Version |
|-----------|-----------|---------|
| Frontend Framework | Streamlit | 1.28.1 |
| Language Model | Claude 3.5 Sonnet | Latest |
| API Client | Anthropic Python SDK | 0.7.1 |
| Language | Python | 3.8+ |
| Environment Management | python-dotenv | 1.0.0 |

### Key Libraries:

- **streamlit**: Web UI framework for rapid application development
- **anthropic**: Official API client for Claude models
- **python-dotenv**: Environment variable management for API keys
- **json**: Data serialization and deserialization
- **re**: Regular expressions for data extraction
- **hashlib**: Secure session ID generation
- **datetime**: Timestamp management

### Model Selection:

**Claude 3.5 Sonnet** was chosen for:
- Superior instruction following and context understanding
- Excellent prompt engineering responsiveness
- Optimal balance of capability and speed
- Strong performance on information extraction tasks
- Reliable JSON output formatting

---

## 🚀 Installation & Setup

### Prerequisites:
- Python 3.8 or higher
- Git
- Anthropic API Key (get it from https://console.anthropic.com/)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd talent-scout
```

### Step 2: Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
```

Replace `your_api_key_here` with your actual Anthropic API key.

### Step 5: Run the Application

```bash
streamlit run hiring_assistant.py
```

The application will open in your browser at `http://localhost:8501`

---

## 📖 Usage Guide

### Starting an Interview:

1. **Launch the Application**: Run `streamlit run hiring_assistant.py`
2. **Read the Greeting**: The chatbot will greet you and explain its purpose
3. **Provide Information**: Answer questions about your background, experience, and tech stack
4. **Answer Technical Questions**: Respond to technical questions generated based on your tech stack
5. **End Interview**: Type "exit", "quit", "bye", or "done" to conclude the interview

### Interview Phases:

#### Phase 1: Greeting
- Chatbot introduces itself
- Explains the purpose of the interview
- Sets expectations

#### Phase 2: Information Gathering
- Name and contact information
- Years of professional experience
- Desired positions
- Current location
- Tech stack (programming languages, frameworks, tools)

#### Phase 3: Technical Assessment
- Dynamic question generation based on tech stack
- Progressive difficulty levels
- Follow-up questions based on answers
- Context-aware responses

#### Phase 4: Conclusion
- Summary of collected information
- Next steps in the hiring process
- Contact information
- Thank you message

### Sidebar Features:

- **Messages Counter**: Track conversation length
- **Interview Phase**: View current conversation stage
- **Extracted Information**: See auto-extracted candidate details
- **Reset Chat**: Start a new interview session
- **Export Data**: Download interview transcript and summary

### Exporting Data:

After interview conclusion, use the Export button to download:
- **JSON Format**: Complete interview data including all messages
- **Markdown Format**: Formatted interview summary for documentation

---

## 🧠 Prompt Design Explanation

### System Prompt Architecture:

The main system prompt is carefully designed with multiple layers:

```python
SYSTEM_PROMPT = """
You are TalentScout, an intelligent Hiring Assistant chatbot...
[Role Definition]

1. Greeting Phase: ...
2. Information Gathering Phase: ...
3. Technical Assessment Phase: ...
[Conversation Phases]

Guidelines:
- Be professional yet friendly
- Ask one or two questions at a time
[Behavioral Guidelines]
"""
```

### Information Gathering Strategy:

**Conversational Approach**: Rather than a form, questions are asked naturally:
- "What's your full name?"
- "How many years have you been in software development?"
- "What technologies are you most comfortable working with?"

**Validation Built-in**: The prompt guides the model to:
- Confirm understood information
- Ask clarifying questions
- Suggest examples if candidate is unclear

### Technical Question Generation:

The technical question prompt:
1. Takes the candidate's tech stack as input
2. Generates questions of progressive difficulty (beginner → intermediate → advanced)
3. Returns structured JSON for easy processing
4. Includes an introductory message

Example output:
```json
{
    "questions": [
        {
            "id": 1,
            "question": "What is a virtual environment in Python and why is it important?",
            "difficulty": "beginner"
        },
        {
            "id": 2,
            "question": "Explain the difference between list comprehension and generator expressions",
            "difficulty": "intermediate"
        }
    ],
    "intro": "Let's assess your Python knowledge with some targeted questions"
}
```

### Context Management:

The system prompt ensures:
- All previous messages are considered in responses
- Information already provided isn't asked again
- Follow-up questions build on previous answers
- Conversation feels natural, not robotic

---

## 🛠️ Challenges & Solutions

### Challenge 1: Information Extraction Accuracy

**Problem**: Extracting structured data from conversational responses

**Solution**:
- Use Claude's JSON output capabilities
- Create dedicated extraction prompts
- Validate extracted data
- Periodic extraction during conversation (every 6 messages)

### Challenge 2: Context Management

**Problem**: Ensuring the model remembers all discussed topics

**Solution**:
- Include full message history in API calls
- Use session state to maintain conversation context
- Implement phase tracking (greeting → info gathering → assessment)

### Challenge 3: Handling Out-of-Scope Input

**Problem**: Users asking irrelevant questions or trying to break the chatbot

**Solution**:
- Design fallback mechanism in system prompt
- Politely redirect off-topic inputs
- Maintain conversation flow
- Keep chatbot focused on hiring purpose

### Challenge 4: Technical Question Relevance

**Problem**: Generating questions appropriate to diverse tech stacks

**Solution**:
- Dynamic prompt generation based on actual tech stack
- Claude's ability to understand various technologies
- Progressive difficulty levels
- Include both theoretical and practical questions

### Challenge 5: Data Privacy & Security

**Problem**: Handling sensitive candidate information securely

**Solution**:
- Data stored in session state (in-memory, cleared on app restart)
- No backend database in local deployment
- Optional: Implement secure backend for production
- Follow GDPR compliance guidelines
- Hash session IDs for anonymity

### Challenge 6: API Rate Limiting & Costs

**Problem**: Managing API costs and rate limits

**Solution**:
- Use efficient models (Claude 3.5 Sonnet)
- Batch data extraction (every 6 messages, not every message)
- Implement error handling with graceful degradation
- Cache extracted information in session state

---

## 📊 Data Flow Diagram

```
┌──────────────────┐
│  User Input      │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Exit Command Check                   │
│ - Detect keywords                    │
│ - If exit: Conclude conversation     │
│ - If continue: Process normally      │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Add to Conversation History          │
│ - User message to session state      │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Call Claude API                      │
│ - Include full message history       │
│ - Use system prompt                  │
│ - Generate contextual response       │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Process Response                     │
│ - Add assistant message to history   │
│ - Extract candidate info (periodic)  │
│ - Update UI                          │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Display Response                     │
│ - Chat message appears               │
│ - Update sidebar metrics             │
│ - Refresh UI                         │
└──────────────────────────────────────┘
```

---

## 🔒 Data Privacy & Compliance

### Current Implementation (Development):
- Data stored in Streamlit session state (in-memory)
- Cleared on app restart or session timeout
- No persistent database
- Suitable for demonstrations and testing

### Production Recommendations:

For production deployment, implement:

1. **Encrypted Storage**:
   ```python
   from cryptography.fernet import Fernet
   
   cipher = Fernet(encryption_key)
   encrypted_data = cipher.encrypt(json.dumps(candidate_info).encode())
   ```

2. **Secure Database**:
   ```python
   import sqlite3
   conn = sqlite3.connect('candidates.db')
   # Use parameterized queries to prevent SQL injection
   ```

3. **GDPR Compliance**:
   - Data retention policies
   - Right to be forgotten implementation
   - Data processing agreements
   - Privacy policy integration

4. **Audit Logging**:
   ```python
   logging.info(f"Session {session_id}: Candidate {name} interview started")
   logging.info(f"Session {session_id}: Data export requested")
   ```

5. **Access Control**:
   - Authentication for admin dashboard
   - Role-based access control
   - Logging of who accessed candidate data

---

## 🚀 Deployment

### Local Deployment:

```bash
streamlit run hiring_assistant.py
```

### Cloud Deployment (AWS):

1. **Deploy to EC2**:
```bash
# Launch EC2 instance
# Install Python, dependencies
# Run Streamlit on port 8501
# Use Nginx as reverse proxy
```

2. **Deploy to Streamlit Cloud**:
```bash
# Push code to GitHub
# Connect repository to Streamlit Cloud
# App auto-deploys on push
# Access via https://your-username-appname.streamlit.app
```

3. **Docker Deployment**:

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "hiring_assistant.py"]
```

Build and run:
```bash
docker build -t talentscout .
docker run -p 8501:8501 -e ANTHROPIC_API_KEY=xxx talentscout
```

---

## 📈 Future Enhancements

### Phase 2 Features:

1. **Sentiment Analysis**:
   - Gauge candidate emotions during interview
   - Identify confidence levels
   - Flag potential concerns

2. **Multilingual Support**:
   - Support interviews in multiple languages
   - Automatic translation
   - Localized technical questions

3. **Resume Integration**:
   - Upload and parse resumes
   - Auto-fill candidate information
   - Cross-reference with interview data

4. **Scoring System**:
   - Automatic candidate scoring
   - Ranking system
   - Recommendation for next round

5. **Integration with ATS**:
   - Connect with Applicant Tracking Systems
   - Auto-submit candidate data
   - Webhook notifications

6. **Video Interview**:
   - Integrate video recording
   - Real-time transcription
   - Video-based sentiment analysis

7. **Analytics Dashboard**:
   - Interview statistics
   - Candidate demographics
   - Conversion rates
   - Time-to-hire metrics

---

## 🐛 Troubleshooting

### Issue: "API Key not found"
**Solution**: Ensure `ANTHROPIC_API_KEY` is set in `.env` file or environment variables

### Issue: "Rate limit exceeded"
**Solution**: Anthropic API has rate limits. Implement exponential backoff:
```python
import time
try:
    response = client.messages.create(...)
except RateLimitError:
    time.sleep(60)  # Wait 60 seconds, then retry
```

### Issue: "Streamlit not found"
**Solution**: Reinstall dependencies: `pip install -r requirements.txt`

### Issue: "Poor response quality"
**Solution**: 
- Refine system prompt
- Provide more context
- Use higher max_tokens
- Adjust temperature if exposed to API

### Issue: "Session state not persisting"
**Solution**: 
- This is normal in Streamlit (rerun on each interaction)
- Use `@st.cache_data` or `@st.cache_resource` for persistence
- For persistent storage, use database backend

---

## 📝 Code Quality Standards

### Structure:
- ✅ Modular functions with single responsibilities
- ✅ Clear variable naming conventions
- ✅ Comprehensive docstrings
- ✅ Error handling with user-friendly messages
- ✅ Comments explaining complex logic

### Best Practices Applied:
- ✅ DRY (Don't Repeat Yourself) principle
- ✅ Configuration management (prompts as constants)
- ✅ Session state management
- ✅ Exception handling
- ✅ Logging (can be enhanced)
- ✅ Input validation and sanitization

---

## 🔗 Additional Resources

- **Streamlit Documentation**: https://docs.streamlit.io/
- **Anthropic API Docs**: https://docs.anthropic.com/
- **Prompt Engineering Guide**: https://www.promptingguide.ai/
- **Python Best Practices**: https://pep8.org/
- **GDPR Compliance**: https://gdpr.eu/
- **Git Guide**: https://guides.github.com/

---

## 📄 License

This project is provided for educational and evaluation purposes.

---

## 👥 Contributing

To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📞 Support

For issues, questions, or suggestions:
- Open an GitHub issue
- Contact: support@talentscout.com
- Documentation: See above sections

---

## 🎓 Learning Outcomes

By studying this project, you'll learn:

1. **Prompt Engineering**:
   - System prompt design
   - Dynamic prompt generation
   - Context management
   - JSON output formatting

2. **Streamlit Development**:
   - UI components and layouts
   - Session state management
   - Chat interfaces
   - File export functionality

3. **API Integration**:
   - Anthropic API usage
   - Error handling
   - Rate limiting management
   - Streaming responses

4. **Software Architecture**:
   - Modular design
   - State management
   - Data flow design
   - Conversation design patterns

5. **Data Privacy**:
   - Sensitive data handling
   - GDPR principles
   - Security best practices
   - Audit logging

---

**Last Updated**: December 2024  
**Version**: 1.0.0  
**Status**: Production Ready ✅