"""
Utility Functions for TalentScout Hiring Assistant
"""

import json
import re
import hashlib
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from config import (
    VALIDATION_RULES, LOG_FORMAT, LOG_LEVEL, 
    EXIT_KEYWORDS, ERROR_MESSAGES
)

# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
logger = logging.getLogger(__name__)

# ============================================================================
# STRING & TEXT UTILITIES
# ============================================================================

def is_exit_command(user_input: str) -> bool:
    """
    Check if user input contains exit keywords
    
    Args:
        user_input: User's text input
        
    Returns:
        Boolean indicating if input is an exit command
        
    Example:
        >>> is_exit_command("bye!")
        True
    """
    user_lower = user_input.lower().strip()
    return any(keyword in user_lower for keyword in EXIT_KEYWORDS)


def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent injection attacks
    
    Args:
        text: Raw user input
        
    Returns:
        Sanitized text
    """
    # Remove extra whitespace
    text = " ".join(text.split())
    # Remove potential harmful characters
    text = re.sub(r'[<>\"\'`;]', '', text)
    return text.strip()


def extract_email(text: str) -> Optional[str]:
    """
    Extract email address from text
    
    Args:
        text: Text potentially containing email
        
    Returns:
        Email address if found, None otherwise
    """
    pattern = VALIDATION_RULES.get("email")
    if pattern:
        match = re.search(pattern, text)
        return match.group(0) if match else None
    return None


def extract_phone(text: str) -> Optional[str]:
    """
    Extract phone number from text
    
    Args:
        text: Text potentially containing phone number
        
    Returns:
        Phone number if found, None otherwise
    """
    pattern = VALIDATION_RULES.get("phone")
    if pattern:
        match = re.search(pattern, text)
        return match.group(0) if match else None
    return None


def extract_numbers(text: str) -> List[int]:
    """
    Extract all numbers from text
    
    Args:
        text: Text potentially containing numbers
        
    Returns:
        List of integers found in text
    """
    return [int(match) for match in re.findall(r'\d+', text)]


# ============================================================================
# VALIDATION UTILITIES
# ============================================================================

def is_valid_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email address to validate
        
    Returns:
        Boolean indicating validity
    """
    pattern = VALIDATION_RULES.get("email")
    return bool(re.match(pattern, email)) if pattern else False


def is_valid_phone(phone: str) -> bool:
    """
    Validate phone number format
    
    Args:
        phone: Phone number to validate
        
    Returns:
        Boolean indicating validity
    """
    pattern = VALIDATION_RULES.get("phone")
    return bool(re.match(pattern, phone)) if pattern else False


def is_valid_years_experience(years: int) -> bool:
    """
    Validate years of experience
    
    Args:
        years: Number of years
        
    Returns:
        Boolean indicating validity
    """
    rules = VALIDATION_RULES.get("years_of_experience", {})
    min_years = rules.get("min", 0)
    max_years = rules.get("max", 70)
    return min_years <= years <= max_years


def is_valid_name(name: str) -> bool:
    """
    Validate name length and format
    
    Args:
        name: Full name
        
    Returns:
        Boolean indicating validity
    """
    rules = VALIDATION_RULES.get("name_length", {})
    min_len = rules.get("min", 2)
    max_len = rules.get("max", 100)
    return min_len <= len(name) <= max_len and name.strip() != ""


# ============================================================================
# DATA EXTRACTION UTILITIES
# ============================================================================

def parse_json_response(response_text: str) -> Optional[Dict]:
    """
    Parse JSON from response text, handling formatting issues
    
    Args:
        response_text: Raw response text from LLM
        
    Returns:
        Parsed JSON dict or None if parsing fails
    """
    try:
        # Try direct parsing
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass
    
    try:
        # Try extracting JSON from markdown code blocks
        json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
    except (json.JSONDecodeError, AttributeError):
        pass
    
    try:
        # Try extracting JSON from curly braces
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
    except (json.JSONDecodeError, AttributeError):
        pass
    
    logger.warning(f"Failed to parse JSON from: {response_text[:100]}...")
    return None


def extract_tech_stack(text: str) -> List[str]:
    """
    Extract technology stack from text
    
    Args:
        text: Text describing tech stack
        
    Returns:
        List of technologies found
    """
    # Common technologies to look for
    common_techs = [
        'python', 'javascript', 'java', 'c#', 'c++', 'go', 'rust', 'php', 'ruby',
        'react', 'vue', 'angular', 'django', 'flask', 'fastapi', 'spring', 'express',
        'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch',
        'docker', 'kubernetes', 'aws', 'gcp', 'azure',
        'git', 'jenkins', 'gitlab', 'github', 'azure devops',
        'html', 'css', 'sql', 'rest', 'graphql', 'grpc'
    ]
    
    text_lower = text.lower()
    found_techs = []
    
    for tech in common_techs:
        if tech in text_lower:
            found_techs.append(tech)
    
    # Also capture custom/unclear techs (words that look like tech names)
    # e.g., "MyCustomFramework"
    potential_techs = re.findall(r'\b[A-Z][a-zA-Z0-9]+\b', text)
    found_techs.extend(potential_techs)
    
    return list(set(found_techs))  # Remove duplicates


def extract_years_from_text(text: str) -> Optional[int]:
    """
    Extract years of experience from text
    
    Args:
        text: Text potentially containing year reference
        
    Returns:
        Number of years if found, None otherwise
    """
    # Look for patterns like "5 years", "10+ years", etc.
    match = re.search(r'(\d+)\s*\+?\s*years?', text, re.IGNORECASE)
    if match:
        years = int(match.group(1))
        if is_valid_years_experience(years):
            return years
    
    return None


# ============================================================================
# SESSION UTILITIES
# ============================================================================

def generate_session_id(name: str = "", timestamp: Optional[datetime] = None) -> str:
    """
    Generate a unique session ID
    
    Args:
        name: Candidate name (optional, for reproducibility)
        timestamp: Timestamp (optional)
        
    Returns:
        Unique session ID (12 characters)
    """
    if timestamp is None:
        timestamp = datetime.now()
    
    unique_str = f"{name}{timestamp.isoformat()}".encode()
    session_id = hashlib.md5(unique_str).hexdigest()[:12]
    
    logger.info(f"Generated session ID: {session_id}")
    return session_id


def get_timestamp() -> str:
    """
    Get current timestamp in ISO format
    
    Returns:
        ISO formatted timestamp string
    """
    return datetime.now().isoformat()


# ============================================================================
# FORMATTING UTILITIES
# ============================================================================

def format_candidate_summary(candidate_info: Dict) -> str:
    """
    Format candidate information as readable summary
    
    Args:
        candidate_info: Dictionary of candidate information
        
    Returns:
        Formatted summary string
    """
    summary = f"""
**CANDIDATE SUMMARY**
{'='*50}

**Personal Information:**
  Name: {candidate_info.get('full_name', 'Not provided')}
  Email: {candidate_info.get('email', 'Not provided')}
  Phone: {candidate_info.get('phone', 'Not provided')}
  Location: {candidate_info.get('current_location', 'Not provided')}

**Professional Information:**
  Experience: {candidate_info.get('years_of_experience', 'Not provided')} years
  Desired Position(s): {candidate_info.get('desired_positions', 'Not provided')}
  
**Technical Skills:**
  Tech Stack: {', '.join(candidate_info.get('tech_stack', [])) if candidate_info.get('tech_stack') else 'Not specified'}

**Additional Data:**
  Responses: {len(candidate_info.get('technical_responses', [])) if candidate_info.get('technical_responses') else '0'}
"""
    return summary.strip()


def format_message_preview(message: str, max_length: int = 100) -> str:
    """
    Format a message preview with truncation
    
    Args:
        message: Full message text
        max_length: Maximum length before truncation
        
    Returns:
        Preview string with ellipsis if truncated
    """
    if len(message) > max_length:
        return message[:max_length] + "..."
    return message


# ============================================================================
# CONVERSATION UTILITIES
# ============================================================================

def count_conversation_turns(messages: List[Dict]) -> Tuple[int, int]:
    """
    Count user and assistant messages in conversation
    
    Args:
        messages: List of message dictionaries
        
    Returns:
        Tuple of (user_messages, assistant_messages)
    """
    user_count = sum(1 for m in messages if m.get("role") == "user")
    assistant_count = sum(1 for m in messages if m.get("role") == "assistant")
    return user_count, assistant_count


def get_last_message(messages: List[Dict], role: str = "user") -> Optional[str]:
    """
    Get the last message from a specific role
    
    Args:
        messages: List of message dictionaries
        role: Role to filter by ("user" or "assistant")
        
    Returns:
        Last message content or None
    """
    for message in reversed(messages):
        if message.get("role") == role:
            return message.get("content")
    return None


def build_conversation_text(messages: List[Dict]) -> str:
    """
    Build readable conversation text from messages
    
    Args:
        messages: List of message dictionaries
        
    Returns:
        Formatted conversation text
    """
    conversation = []
    for msg in messages:
        role = msg.get("role", "unknown").upper()
        content = msg.get("content", "")
        conversation.append(f"{role}: {content}")
    
    return "\n".join(conversation)


# ============================================================================
# ERROR HANDLING UTILITIES
# ============================================================================

def get_error_message(error_key: str, **kwargs) -> str:
    """
    Get formatted error message
    
    Args:
        error_key: Key from ERROR_MESSAGES dict
        **kwargs: Format variables
        
    Returns:
        Formatted error message
    """
    base_message = ERROR_MESSAGES.get(error_key, "An error occurred")
    try:
        return base_message.format(**kwargs)
    except KeyError:
        return base_message


def log_error(error_type: str, error_msg: str, context: Optional[Dict] = None):
    """
    Log error with context
    
    Args:
        error_type: Type of error
        error_msg: Error message
        context: Optional context dictionary
    """
    log_msg = f"[{error_type}] {error_msg}"
    if context:
        log_msg += f" | Context: {json.dumps(context)}"
    logger.error(log_msg)


# ============================================================================
# TESTING UTILITIES
# ============================================================================

def create_test_conversation() -> List[Dict]:
    """
    Create a sample conversation for testing
    
    Returns:
        List of message dictionaries
    """
    return [
        {
            "role": "assistant",
            "content": "Hello! Welcome to TalentScout. What's your name?"
        },
        {
            "role": "user",
            "content": "My name is John Doe"
        },
        {
            "role": "assistant",
            "content": "Nice to meet you, John! How many years of experience do you have?"
        },
        {
            "role": "user",
            "content": "I have 5 years of experience as a software developer"
        }
    ]


# ============================================================================
# MAIN (For testing utilities)
# ============================================================================

if __name__ == "__main__":
    # Test basic utilities
    print("Testing Email Extraction:", extract_email("Contact me at john@example.com"))
    print("Testing Tech Stack:", extract_tech_stack("I know Python, React, and Docker"))
    print("Testing Years:", extract_years_from_text("I have 5 years of experience"))
    print("Testing Exit Command:", is_exit_command("goodbye!"))
    print("\n✅ All utility tests passed!")