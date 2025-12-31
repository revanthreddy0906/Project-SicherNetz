import sqlite3
import os
import bcrypt

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")


def get_db():
    return sqlite3.connect(DB_PATH)


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


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt.
    """
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def verify_password(password: str, stored_password: str) -> bool:
    """
    Verify a password against a stored bcrypt hash
    or legacy plaintext password.
    """
    if stored_password.startswith("$2"):
        return bcrypt.checkpw(
            password.encode(),
            stored_password.encode()
        )

    # legacy SHA256
    return stored_password == hashlib.sha256(password.encode()).hexdigest()


def add_user(username, password_hash, group_name):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "INSERT OR REPLACE INTO users VALUES (?, ?, ?)",
        (username, password_hash, group_name)
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

    if verify_password(password, stored_hash):
        return group

    return None
