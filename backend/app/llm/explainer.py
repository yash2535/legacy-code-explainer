from backend.app.llm.client import call_llm
from typing import Optional


def explain(ir: dict, language: str = "cobol") -> str:
    """
    Generates a natural language explanation strictly based on IR.
    This explainer is LIMITED to COBOL and JCL only.
    
    Args:
        ir (dict): Intermediate representation containing program structure
        language (str): Target language - "cobol" or "jcl" (default: "cobol")
    
    Returns:
        str: Natural language explanation of the program
        
    Raises:
        ValueError: If language is not COBOL or JCL
        TypeError: If ir is not a dictionary
    """
    
    # -------------------------------------------------
    # 🔍 INPUT VALIDATION
    # -------------------------------------------------
    if not isinstance(ir, dict):
        raise TypeError(f"IR must be a dictionary, got {type(ir).__name__}")
    
    language = language.lower().strip()
    
    if language not in {"cobol", "jcl"}:
        raise ValueError(
            f"Unsupported language: '{language}'. "
            "This explainer supports ONLY COBOL and JCL."
        )
    
    # -------------------------------------------------
    # 🧾 JCL EXPLANATION (NO EXAMPLES – STRUCTURAL ONLY)
    # -------------------------------------------------
    if language == "jcl":
        return _explain_jcl(ir)
    
    # -------------------------------------------------
    # 🧠 COBOL EXPLANATION WITH SAFE EXAMPLES
    # -------------------------------------------------
    return _explain_cobol(ir)


def _explain_jcl(ir: dict) -> str:
    """
    Generates JCL-specific explanation.
    
    Args:
        ir (dict): JCL intermediate representation
        
    Returns:
        str: JCL explanation
    """
    
    prompt = f"""
You are a senior IBM Mainframe JCL engineer.

STRICT RULES (MANDATORY):
- Explain ONLY the JCL job described below.
- Do NOT invent steps, datasets, or utilities.
- Do NOT explain COBOL, SQL, or business logic.
- Do NOT give examples.
- Use standard JCL terminology only.
- Provide a concise, step-by-step explanation of the JOB, EXEC steps, and DD statements.

JCL INTERMEDIATE REPRESENTATION (IR):
{ir}

Provide a clear, professional explanation of this JCL job structure.
"""
    
    try:
        result = call_llm(prompt).strip()
        return result
    except Exception as e:
        return f"ERROR: Failed to generate JCL explanation: {str(e)}"


def _explain_cobol(ir: dict) -> str:
    """
    Generates COBOL-specific explanation with conditional section inclusion.
    
    Args:
        ir (dict): COBOL intermediate representation
        
    Returns:
        str: COBOL explanation
    """
    
    # Extract IR components with safe defaults
    program_id = ir.get("program_info", {}).get("program_id", "UNKNOWN")
    statements = ir.get("statements", [])
    control_flow = ir.get("control_flow", [])
    file_ops = ir.get("file_operations", [])
    arithmetic_ops = ir.get("arithmetic_operations", [])
    
    # Build dynamic prompt - only include sections with data
    prompt = f"""
You are a senior IBM Mainframe COBOL engineer.

========================
MANDATORY RULES (STRICT)
========================
- Explain ONLY what is explicitly present in the IR.
- Treat this as STATIC CODE ANALYSIS, not program execution.
- Do NOT assume runtime values or evaluate conditions.
- Do NOT say which branch "will" or "will not" execute.
- Do NOT invent missing statements, paragraphs, or logic.
- Do NOT reference line numbers or missing lines.
- Use professional COBOL batch terminology only.
- Do NOT provide theoretical or hypothetical examples.
- Do NOT mention constructs that are not present in the IR.

========================
CONTROL FLOW RULES
========================
- Explain IF statements in terms of POSSIBLE BRANCHES only if control flow is present.
- Use wording such as:
  "If the condition is satisfied, the following actions occur..."
  "Otherwise, an alternate path is available..."
- Never flatten IF/ELSE logic into sequential steps.

========================
EXAMPLE RULES
========================
- CRITICAL: Give examples ONLY if arithmetic operations appear in the IR section below.
- Do NOT provide hypothetical, theoretical, or "what if" examples.
- Use ONE simple numeric example per arithmetic operation only.
- Do NOT give examples for DISPLAY, MOVE, STOP RUN, PERFORM, or FILE I/O.
- If no arithmetic operations section appears below, provide NO examples whatsoever.

========================
INPUT (INTERMEDIATE REPRESENTATION)
========================

COBOL PROGRAM NAME:
{program_id}

EXECUTABLE STRUCTURE:
{statements}
"""
    
    # Conditionally add control flow section
    if control_flow:
        prompt += f"\nCONTROL FLOW STRUCTURE:\n{control_flow}\n"
    
    # Conditionally add file operations section
    if file_ops:
        prompt += f"\nFILE OPERATIONS:\n{file_ops}\n"
    
    # Conditionally add arithmetic operations section
    if arithmetic_ops:
        prompt += f"\nARITHMETIC OPERATIONS:\n{arithmetic_ops}\n"
    
    # Add task and output requirements
    prompt += """
========================
TASK
========================
1. Describe the overall program purpose at a high level.
2. Explain the program flow using semantic blocks (not line-by-line).
3. If a CONTROL FLOW STRUCTURE section appears above, explain conditional logic using branch-based descriptions.
4. If a FILE OPERATIONS section appears above, describe file handling.
5. If an ARITHMETIC OPERATIONS section appears above, mention them and provide ONE example.
6. If a section does not appear above, do NOT mention it or provide examples for it.

OUTPUT REQUIREMENTS:
- One cohesive, professional explanation.
- No bullet-point tutorials.
- No speculative behavior.
- No execution assumptions.
- No mention of absent sections.
- No hypothetical examples.
"""
    
    try:
        result = call_llm(prompt).strip()
        return result
    except Exception as e:
        return f"ERROR: Failed to generate COBOL explanation: {str(e)}"