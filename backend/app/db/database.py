import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "chat.db")

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        language TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ir_store (
        session_id TEXT PRIMARY KEY,
        ir_json TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS chat_messages (
        session_id TEXT,
        role TEXT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()
