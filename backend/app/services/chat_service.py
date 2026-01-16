import json
from backend.app.db.database import get_connection

def save_session(session_id, language):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO sessions VALUES (?, ?)",
        (session_id, language)
    )
    conn.commit()
    conn.close()


def save_ir(session_id, ir):
    if ir is None:
        raise ValueError("IR is None — pipeline did not return IR")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR REPLACE INTO ir_store (session_id, ir_json)
        VALUES (?, ?)
        """,
        (session_id, json.dumps(ir))
    )

    conn.commit()
    conn.close()




def load_ir(session_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT ir_json FROM ir_store WHERE session_id = ?",
        (session_id,)
    )

    row = cur.fetchone()
    conn.close()

    if not row or not row[0]:
        return None

    return json.loads(row[0])



def save_message(session_id, role, message):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chat_messages VALUES (?, ?, ?)",
        (session_id, role, message)
    )
    conn.commit()
    conn.close()
