import re
from typing import Dict, List, Any
from backend.app.parsers.base_parser import BaseParser
from backend.app.core.ir_schema.ir import empty_cobol_ir


class CobolRegexParser(BaseParser):
    """
    Regex-based COBOL parser (V1 – Stable)

    Features:
    - Program info extraction
    - Division detection
    - Variable extraction
    - Paragraph detection
    - Statement extraction (DISPLAY, ACCEPT, MOVE, COMPUTE, ADD, MULTIPLY, STOP)
    - Control flow extraction (IF, PERFORM, EVALUATE, GO TO)
    - File operation detection
    """

    # ==========================================================
    # PUBLIC API
    # ==========================================================

    def parse(self, code: str) -> Dict[str, Any]:
        # Always start with a fresh IR for every parse call
        self.ir = empty_cobol_ir()

        code = self._normalize_code(code)
        lines = code.split("\n")

        self._extract_program_info(code)
        self._extract_divisions(code)
        self._extract_variables(code)
        self._extract_paragraphs(lines)
        self._extract_statements(lines)
        self._extract_control_flow(lines)
        self._extract_file_operations(lines)
        self._extract_performs(code)

        # Warning if no executable logic
        if not any([
            self.ir["statements"],
            self.ir["control_flow"],
            self.ir["file_operations"]
        ]):
            self.ir["warnings"].append(
                "No executable logic detected. Program may be declarative only."
            )

        return self.ir

    def get_ir(self) -> Dict[str, Any]:
        return self.ir

    # ==========================================================
    # NORMALIZATION
    # ==========================================================

    def _normalize_code(self, code: str) -> str:
        """
        Normalize COBOL source:
        - Remove comments
        - Handle fixed & free format
        - Convert to uppercase
        """
        lines = []

        for line in code.split("\n"):
            raw = line.rstrip()

            # Skip comment lines
            if raw.lstrip().startswith("*"):
                continue

            # Remove sequence numbers (fixed format)
            if len(raw) >= 7 and raw[:6].isdigit():
                raw = raw[6:]

            lines.append(raw.upper())

        return "\n".join(lines)

    # ==========================================================
    # PROGRAM INFO
    # ==========================================================

    def _extract_program_info(self, code: str):
        m = re.search(r"PROGRAM-ID\.\s+([A-Z0-9\-]+)", code)
        if m:
            self.ir["program_info"]["program_id"] = m.group(1)

    # ==========================================================
    # DIVISIONS
    # ==========================================================

    def _extract_divisions(self, code: str):
        divisions = [
            "IDENTIFICATION DIVISION",
            "ENVIRONMENT DIVISION",
            "DATA DIVISION",
            "PROCEDURE DIVISION"
        ]

        for div in divisions:
            if div in code:
                self.ir["divisions"][div.lower().replace(" ", "_")] = True

    # ==========================================================
    # VARIABLES
    # ==========================================================

    def _extract_variables(self, code: str):
        pattern = r"^\s*(\d{2})\s+([A-Z0-9\-]+)\s+(PIC|PICTURE)\s+([^\s\.]+)"
        for m in re.finditer(pattern, code, re.MULTILINE):
            self.ir["variables"].append({
                "level": m.group(1),
                "name": m.group(2),
                "picture": m.group(4)
            })

    # ==========================================================
    # PARAGRAPHS
    # ==========================================================

    def _extract_paragraphs(self, lines: List[str]):
        in_procedure = False

        for i, line in enumerate(lines):
            if "PROCEDURE DIVISION" in line:
                in_procedure = True
                continue

            if not in_procedure or "SECTION" in line:
                continue

            m = re.match(r"\s*([A-Z][A-Z0-9\-]*)\.", line)
            if m:
                name = m.group(1)
                if name not in ["END-IF", "ELSE", "END-PERFORM"]:
                    self.ir["paragraphs"].append({
                        "id": f"PARA_{i + 1}",
                        "name": name,
                        "line": i + 1
                    })

    # ==========================================================
    # STATEMENTS (EXECUTABLE)
    # ==========================================================

    def _extract_statements(self, lines: List[str]):
        for i, line in enumerate(lines):

            # DISPLAY
            if m := re.search(r"\bDISPLAY\s+(.+?)(?:\.|$)", line):
                self.ir["statements"].append({
                    "type": "DISPLAY",
                    "id": f"STMT_{i + 1}",
                    "value": m.group(1),
                    "line": i + 1
                })

            # ACCEPT (User Input)
            elif m := re.search(r"\bACCEPT\s+([A-Z0-9\-]+)", line):
                self.ir["statements"].append({
                    "type": "ACCEPT",
                    "id": f"STMT_{i + 1}",
                    "target": m.group(1),
                    "line": i + 1
                })

            # MOVE
            elif m := re.search(r"\bMOVE\s+(.+?)\s+TO\s+(.+?)\.", line):
                self.ir["statements"].append({
                    "type": "MOVE",
                    "id": f"STMT_{i + 1}",
                    "from": m.group(1),
                    "to": m.group(2),
                    "line": i + 1
                })

            # COMPUTE (Arithmetic)
            elif m := re.search(r"\bCOMPUTE\s+(.+?)\s*=\s*(.+?)\.", line):
                self.ir["statements"].append({
                    "type": "COMPUTE",
                    "id": f"STMT_{i + 1}",
                    "target": m.group(1),
                    "expression": m.group(2),
                    "line": i + 1
                })

            # ADD
            elif m := re.search(r"\bADD\s+(.+?)\s+GIVING\s+(.+?)\.", line):
                self.ir["statements"].append({
                    "type": "ADD",
                    "id": f"STMT_{i + 1}",
                    "operands": m.group(1),
                    "result": m.group(2),
                    "line": i + 1
                })

            # MULTIPLY
            elif m := re.search(
                r"\bMULTIPLY\s+(.+?)\s+BY\s+(.+?)\s+GIVING\s+(.+?)\.",
                line
            ):
                self.ir["statements"].append({
                    "type": "MULTIPLY",
                    "id": f"STMT_{i + 1}",
                    "left": m.group(1),
                    "right": m.group(2),
                    "result": m.group(3),
                    "line": i + 1
                })

            # STOP RUN
            elif "STOP RUN" in line:
                self.ir["statements"].append({
                    "type": "STOP",
                    "id": f"STMT_{i + 1}",
                    "line": i + 1
                })

    # ==========================================================
    # CONTROL FLOW
    # ==========================================================
    def _extract_control_flow(self, lines: List[str]):
        for i, line in enumerate(lines):

            # IF condition
            if m := re.search(r"\bIF\s+(.+?)(?:THEN|$)", line):
                self.ir["control_flow"].append({
                    "id": f"CF_{i + 1}",
                    "type": "IF",
                    "condition": m.group(1),
                    "line": i + 1
                })
                self.ir["conditions"].append(m.group(1))

        # PERFORM
            elif m := re.search(r"\bPERFORM\s+(.+?)\.", line):
                self.ir["control_flow"].append({
                    "id": f"CF_{i + 1}",
                    "type": "PERFORM",
                    "target": m.group(1),
                    "line": i + 1
                })

        # EVALUATE
            elif m := re.search(r"\bEVALUATE\s+(.+)", line):
                self.ir["control_flow"].append({
                    "id": f"CF_{i + 1}",
                    "type": "EVALUATE",
                    "expression": m.group(1),
                    "line": i + 1
                })

        # GO TO
            elif m := re.search(r"\bGO\s+TO\s+([A-Z0-9\-]+)", line):
                self.ir["control_flow"].append({
                    "id": f"CF_{i + 1}",
                    "type": "GO_TO",
                    "target": m.group(1),
                    "line": i + 1
                })

    # ==========================================================
    # FILE OPERATIONS
    # ==========================================================

    def _extract_file_operations(self, lines: List[str]):
        for i, line in enumerate(lines):
            if m := re.search(r"\b(OPEN|READ|WRITE|CLOSE|DELETE|REWRITE)\b", line):
                self.ir["file_operations"].append({
                    "operation": m.group(1),
                    "line": i + 1
                })

    # ==========================================================
    # PERFORM CALL GRAPH
    # ==========================================================

    def _extract_performs(self, code: str):
        lines = code.split("\n")

        for i, line in enumerate(lines):
            if m := re.search(r"\bPERFORM\s+([A-Z0-9\-]+)", line):
                self.ir["performs"].append({
                    "id": f"PERFORM_{i + 1}",
                    "target": m.group(1),
                    "line": i + 1
                })
