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

    # legacy fallback (temporary)
    return password == stored_password


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

    if not row:
        conn.close()
        return None

    stored_password, group = row

    # bcrypt user
    if stored_password.startswith("$2"):
        if not verify_password(password, stored_password):
            conn.close()
            return None

    # legacy user → verify then migrate
    else:
        if password != stored_password:
            conn.close()
            return None

        # 🔁 MIGRATE PASSWORD
        new_hash = hash_password(password)
        c.execute(
            "UPDATE users SET password_hash=? WHERE username=?",
            (new_hash, username)
        )
        conn.commit()

    conn.close()
    return group
