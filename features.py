"""
Advanced Features: Sentiment Analysis & Multilingual Support
"""

import google.generativeai as genai
import config

# ============================================================================
# SUPPORTED LANGUAGES
# ============================================================================

SUPPORTED_LANGUAGES = {
    "English":    {"code": "en", "flag": "🇺🇸", "native": "English"},
    "Hindi":      {"code": "hi", "flag": "🇮🇳", "native": "हिन्दी"},
    "Spanish":    {"code": "es", "flag": "🇪🇸", "native": "Español"},
    "French":     {"code": "fr", "flag": "🇫🇷", "native": "Français"},
    "German":     {"code": "de", "flag": "🇩🇪", "native": "Deutsch"},
    "Arabic":     {"code": "ar", "flag": "🇸🇦", "native": "العربية"},
    "Chinese":    {"code": "zh", "flag": "🇨🇳", "native": "中文"},
    "Japanese":   {"code": "ja", "flag": "🇯🇵", "native": "日本語"},
    "Portuguese": {"code": "pt", "flag": "🇧🇷", "native": "Português"},
}

# ============================================================================
# SENTIMENT ANALYSIS
# ============================================================================

SENTIMENT_LABELS = {
    "confident":   {"emoji": "😊", "color": "#10b981", "label": "Confident"},
    "nervous":     {"emoji": "😰", "color": "#f59e0b", "label": "Nervous"},
    "excited":     {"emoji": "🤩", "color": "#8b5cf6", "label": "Excited"},
    "confused":    {"emoji": "😕", "color": "#ef4444", "label": "Confused"},
    "neutral":     {"emoji": "😐", "color": "#64748b", "label": "Neutral"},
    "frustrated":  {"emoji": "😤", "color": "#f97316", "label": "Frustrated"},
    "enthusiastic":{"emoji": "🚀", "color": "#06b6d4", "label": "Enthusiastic"},
}

SENTIMENT_PROMPT = """Analyze the emotional tone of this candidate message in a job interview context.
Return ONLY one of these labels (lowercase): confident, nervous, excited, confused, neutral, frustrated, enthusiastic

Message: "{message}"

Respond with just the single word label."""


def analyze_sentiment(message: str) -> dict:
    """Analyze sentiment of a candidate message using Gemini."""
    try:
        model = genai.GenerativeModel(
            model_name=config.MODEL,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=10,
                temperature=0.1,
            )
        )
        response = model.generate_content(
            SENTIMENT_PROMPT.format(message=message[:500])
        )
        label = response.text.strip().lower().split()[0]
        return SENTIMENT_LABELS.get(label, SENTIMENT_LABELS["neutral"])
    except Exception:
        return SENTIMENT_LABELS["neutral"]


def get_sentiment_history_summary(sentiment_history: list) -> dict:
    """Summarise sentiment trends from a list of sentiment dicts."""
    if not sentiment_history:
        return {"dominant": SENTIMENT_LABELS["neutral"], "trend": "stable"}

    counts = {}
    for s in sentiment_history:
        lbl = s.get("label", "Neutral")
        counts[lbl] = counts.get(lbl, 0) + 1

    dominant_label = max(counts, key=counts.get)
    dominant = next(
        (v for v in SENTIMENT_LABELS.values() if v["label"] == dominant_label),
        SENTIMENT_LABELS["neutral"]
    )

    # Simple trend: compare last 3 vs first 3
    positive_set = {"Confident", "Excited", "Enthusiastic"}
    recent = sentiment_history[-3:]
    early  = sentiment_history[:3]
    recent_score = sum(1 for s in recent if s.get("label") in positive_set)
    early_score  = sum(1 for s in early  if s.get("label") in positive_set)
    trend = "improving" if recent_score > early_score else (
            "declining"  if recent_score < early_score else "stable")

    return {"dominant": dominant, "trend": trend, "counts": counts}


# ============================================================================
# MULTILINGUAL SYSTEM PROMPT
# ============================================================================

def get_multilingual_system_prompt(base_prompt: str, language: str) -> str:
    """Append language instruction to the base system prompt."""
    if language == "English":
        return base_prompt
    lang_info = SUPPORTED_LANGUAGES.get(language, SUPPORTED_LANGUAGES["English"])
    return (
        base_prompt
        + f"\n\nIMPORTANT: Conduct this entire conversation in {language} ({lang_info['native']}). "
        f"All your responses must be in {language}. "
        f"If the candidate writes in another language, respond in {language} while being helpful."
    )


# ============================================================================
# PERSONALIZED GREETING
# ============================================================================

def build_personalized_context(past_sessions: list) -> str:
    """Build a personalisation note for the system prompt from past sessions."""
    if not past_sessions:
        return ""
    names = [s.get("candidate_name") for s in past_sessions if s.get("candidate_name")]
    if not names:
        return ""
    latest = past_sessions[0]
    name   = latest.get("candidate_name", "")
    date   = latest.get("session_date", "")[:10]
    return (
        f"\n\nPersonalisation context: This recruiter has previously interviewed '{name}' "
        f"(most recent session on {date}). Greet them warmly and acknowledge their experience "
        f"reviewing candidates. Keep it brief and professional."
    )
