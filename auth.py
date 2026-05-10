"""
auth.py — User Authentication Module for TalentScout
Handles signup, login, and session storage using SQLite + bcrypt.
"""

import sqlite3
import bcrypt
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "talentscout.db")


# ============================================================================
# DATABASE INITIALISATION
# ============================================================================

def init_db():
    """Create the users and sessions tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT    UNIQUE NOT NULL,
            email         TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id        INTEGER NOT NULL,
            username       TEXT    NOT NULL,
            session_date   TEXT    NOT NULL,
            messages_count INTEGER DEFAULT 0,
            candidate_name TEXT,
            candidate_role TEXT,
            tech_stack     TEXT,
            chat_export    TEXT,   -- JSON blob of all messages
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


# ============================================================================
# USER MANAGEMENT
# ============================================================================

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def check_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def signup(username: str, email: str, password: str) -> tuple[bool, str]:
    """
    Register a new user.
    Returns (True, success_msg) or (False, error_msg).
    """
    if not username or not email or not password:
        return False, "All fields are required."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (username.strip(), email.strip().lower(), hash_password(password), datetime.now().isoformat())
        )
        conn.commit()
        return True, f"Account created! Welcome, {username} 🎉"
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            return False, "Username already taken."
        return False, "Email already registered."
    finally:
        conn.close()


def login(username: str, password: str) -> tuple[bool, str, dict]:
    """
    Authenticate a user.
    Returns (True, success_msg, user_dict) or (False, error_msg, {}).
    """
    if not username or not password:
        return False, "Username and password are required.", {}

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, username, email, password_hash FROM users WHERE username = ?", (username.strip(),))
    row = cur.fetchone()
    conn.close()

    if not row:
        return False, "User not found.", {}

    user_id, uname, email, pw_hash = row
    if not check_password(password, pw_hash):
        return False, "Incorrect password.", {}

    return True, f"Welcome back, {uname}! 👋", {"id": user_id, "username": uname, "email": email}


# ============================================================================
# SESSION STORAGE
# ============================================================================

def save_session(user_id: int, username: str, messages: list, candidate_info: dict):
    """Persist a completed interview session to the DB."""
    import json

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    tech = candidate_info.get("tech_stack", [])
    tech_str = ", ".join(tech) if isinstance(tech, list) else str(tech)

    cur.execute("""
        INSERT INTO sessions
            (user_id, username, session_date, messages_count, candidate_name, candidate_role, tech_stack, chat_export)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        username,
        datetime.now().isoformat(),
        len(messages),
        candidate_info.get("full_name", ""),
        candidate_info.get("desired_positions", ""),
        tech_str,
        json.dumps(messages)
    ))
    conn.commit()
    conn.close()


def get_user_sessions(user_id: int) -> list[dict]:
    """Fetch all past sessions for a user."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM sessions WHERE user_id = ? ORDER BY session_date DESC",
        (user_id,)
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


# Ensure DB is set up when module is imported
init_db()
