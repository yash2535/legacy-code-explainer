def empty_cobol_ir():
    return {
        "program_info": {},        # PROGRAM-ID, author, etc.
        "divisions": {},            # identification_division, etc.
        "variables": [],            # Working-storage variables
        "paragraphs": [],           # Paragraph names + line numbers
        "statements": [],           # DISPLAY, MOVE, COMPUTE, etc.
        "control_flow": [],         # IF, PERFORM, EVALUATE, GO TO
        "conditions": [],           # IF conditions only
        "file_operations": [],      # READ, WRITE, OPEN, CLOSE
        "performs": [],             # PERFORM call graph
        "warnings": []               # Parser warnings
    }
