from dotenv import load_dotenv
load_dotenv()

import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.app.core.engine import run_pipeline
from backend.app.core.code_detector import detect_code_type
from backend.app.db.database import init_db
from backend.app.services.chat_service import (
    save_session,
    save_ir,
    load_ir,
    save_message
)
from backend.app.llm.explainer import explain_with_query

# -----------------------------
# Initialize DB
# -----------------------------
init_db()

# -----------------------------
# App Init
# -----------------------------
app = FastAPI(
    title="Legacy Code Explainer",
    version="1.1"
)

# -----------------------------
# Request Models
# -----------------------------
class CodeRequest(BaseModel):
    code: str
    language: str | None = None  # optional (auto-detect)


class ChatRequest(BaseModel):
    session_id: str
    user_message: str


# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
def health_check():
    return {"status": "Backend is running"}


# -----------------------------
# Analyze Endpoint
# -----------------------------
@app.post("/analyze")
def analyze_code(request: CodeRequest):

    # 1️⃣ Validate input
    if not request.code or not request.code.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter COBOL or JCL code."
        )

    # 2️⃣ Detect language
    detected_language = request.language or detect_code_type(request.code)
    if not detected_language:
        raise HTTPException(
            status_code=400,
            detail="Please enter valid COBOL or JCL code."
        )

    # 3️⃣ Run pipeline (PARSE + ANALYZE + EXPLAIN)
    result = run_pipeline(
        code=request.code,
        language=detected_language
    )

    # -----------------------------
    # 🔑 SAFE EXTRACTION
    # -----------------------------
    ir = (
        result.get("ir")
        or result.get("intermediate_representation")
        or {}
    )

    analysis = result.get("analysis", {})
    explanation = result.get("explanation", "")

    # 4️⃣ Create session
    session_id = str(uuid.uuid4())
    print("ANALYZE → session_id:", session_id)

    # 5️⃣ Persist session & IR (for chat)
    save_session(session_id, detected_language)
    save_ir(session_id, ir)

    # 6️⃣ Return EVERYTHING (UI + Chat both satisfied)
    return {
        "session_id": session_id,
        "language": detected_language,
        "explanation": explanation,
        "intermediate_representation": ir,
        "analysis": analysis
    }


# -----------------------------
# Chat Endpoint
# -----------------------------
@app.post("/chat")
def chat(request: ChatRequest):

    print("CHAT → received session_id:", request.session_id)

    # 1️⃣ Load IR
    ir = load_ir(request.session_id)
    print("CHAT → IR found:", ir is not None)

    if not ir:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired session."
        )

    # 2️⃣ Save user message
    save_message(request.session_id, "user", request.user_message)

    # 3️⃣ Generate IR-grounded reply
    reply = explain_with_query(
        ir=ir,
        user_query=request.user_message,
        language="cobol"  # can be fetched from DB later
    )

    # 4️⃣ Save assistant reply
    save_message(request.session_id, "assistant", reply)

    return {"reply": reply}
