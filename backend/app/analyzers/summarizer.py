def summarize(ir: dict) -> dict:
    statements = ir.get("statements", [])
    control_flow = ir.get("control_flow", [])
    file_ops = ir.get("file_operations", [])

    summary = {
        # -----------------------------
        # PROGRAM STRUCTURE
        # -----------------------------
        "program_id": ir.get("program_info", {}).get("program_id", "UNKNOWN"),
        "divisions_present": list(ir.get("divisions", {}).keys()),

        # -----------------------------
        # VARIABLES
        # -----------------------------
        "total_variables": len(ir.get("variables", [])),

        # -----------------------------
        # STATEMENTS
        # -----------------------------
        "total_statements": len(statements),
        "statement_types": {
            stmt["type"]: sum(
                1 for s in statements if s["type"] == stmt["type"]
            )
            for stmt in statements
        },

        # -----------------------------
        # CONTROL FLOW
        # -----------------------------
        "total_conditions": len(ir.get("conditions", [])),
        "if_statements": sum(
            1 for c in control_flow if c.get("type") == "IF"
        ),
        "perform_statements": sum(
            1 for c in control_flow if c.get("type") == "PERFORM"
        ),
        "evaluate_statements": sum(
            1 for c in control_flow if c.get("type") == "EVALUATE"
        ),
        "goto_statements": sum(
            1 for c in control_flow if c.get("type") == "GO_TO"
        ),

        # -----------------------------
        # FILE OPERATIONS
        # -----------------------------
        "total_file_operations": len(file_ops),
        "file_operation_types": {
            op["operation"]: sum(
                1 for f in file_ops if f["operation"] == op["operation"]
            )
            for op in file_ops
        },

        # -----------------------------
        # PROCEDURE STRUCTURE
        # -----------------------------
        "total_paragraphs": len(ir.get("paragraphs", [])),
        "total_performs": len(ir.get("performs", [])),

        # -----------------------------
        # WARNINGS
        # -----------------------------
        "warnings": ir.get("warnings", [])
    }

    return summary
