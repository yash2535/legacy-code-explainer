import re
from typing import Optional


def detect_code_type(code: str) -> Optional[str]:
    """
    Detect input code type.
    Returns: 'cobol', 'jcl', or None
    """

    if not code or not code.strip():
        return None

    code_upper = code.upper()

    # ---------------- JCL ----------------
    if re.search(r"^//\w+", code_upper, re.MULTILINE):
        if " JOB " in code_upper or " EXEC " in code_upper:
            return "jcl"

    # ---------------- COBOL ----------------
    cobol_markers = [
        "IDENTIFICATION DIVISION",
        "PROGRAM-ID",
        "DATA DIVISION",
        "PROCEDURE DIVISION"
    ]

    for marker in cobol_markers:
        if marker in code_upper:
            return "cobol"

    return None
