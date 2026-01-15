from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.app.core.engine import run_pipeline
from backend.app.core.code_detector import detect_code_type

app = FastAPI(
    title="Legacy Code Explainer",
    version="1.0"
)

# -----------------------------
# Request Model
# -----------------------------
class CodeRequest(BaseModel):
    code: str
    language: str | None = None   # Optional now


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
    # 1. Validate input
    if not request.code or not request.code.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter COBOL or JCL code."
        )

    # 2. Auto-detect language
    detected_language = detect_code_type(request.code)

    if not detected_language:
        raise HTTPException(
            status_code=400,
            detail="Please enter COBOL or JCL code."
        )

    # 3. Run pipeline
    result = run_pipeline(
        code=request.code,
        language=detected_language
    )

    return result
