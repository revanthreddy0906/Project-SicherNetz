import sqlite3
import hashlib
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

def get_db():
    return sqlite3.connect(DB_PATH)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            group_name TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_user(username, password, group_name):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "INSERT OR REPLACE INTO users VALUES (?, ?, ?)",
        (username, hash_password(password), group_name)
    )
    conn.commit()
    conn.close()

def authenticate(username, password):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "SELECT password_hash, group_name FROM users WHERE username=?",
        (username,)
    )
    row = c.fetchone()
    conn.close()

    if not row:
        return None

    stored_hash, group = row
    return group if stored_hash == hash_password(password) else None
