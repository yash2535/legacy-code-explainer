from backend.app.parsers.base_parser import BaseParser
from typing import Dict, Any, List, Optional
import re


class JCLParser(BaseParser):
    """
    JCL Parser with its OWN IR (independent of COBOL).
    """

    def __init__(self):
        self.ir = {}

    def parse(self, code: str) -> Dict[str, Any]:
        self.ir = {
            "job": {},
            "steps": [],
            "datasets": [],
            "warnings": []
        }

        lines = code.splitlines()
        current_step = None

        for line in lines:
            line = line.rstrip()
            if not line.startswith("//"):
                continue

            # JOB card
            if " JOB " in line:
                self.ir["job"] = self._parse_job_card(line)

            # EXEC step
            elif " EXEC " in line:
                current_step = self._parse_exec_card(line)
                self.ir["steps"].append(current_step)

            # DD statement
            elif " DD " in line and current_step:
                dd = self._parse_dd_card(line)
                current_step["dds"].append(dd)
                if dd.get("dsn"):
                    self.ir["datasets"].append(dd["dsn"])

        self._validate()
        return self.ir

    def get_ir(self) -> Dict[str, Any]:
        """Required by BaseParser"""
        return self.ir

    # ---------------- helpers ----------------

    def _parse_job_card(self, line: str) -> Dict[str, Any]:
        parts = line[2:].split()
        return {
            "name": parts[0],
            "class": self._extract(line, r"CLASS=([A-Z0-9])"),
            "msgclass": self._extract(line, r"MSGCLASS=([A-Z0-9])"),
            "notify": self._extract(line, r"NOTIFY=([A-Z0-9_.]+)"),
            "raw": line
        }

    def _parse_exec_card(self, line: str) -> Dict[str, Any]:
        parts = line[2:].split()
        return {
            "name": parts[0],
            "program": self._extract(line, r"PGM=([A-Z0-9$#@.]+)"),
            "procedure": self._extract(line, r"PROC=([A-Z0-9]+)"),
            "cond": self._extract(line, r"COND=([^,]+)"),
            "dds": [],
            "raw": line
        }

    def _parse_dd_card(self, line: str) -> Dict[str, Any]:
        parts = line[2:].split()
        return {
            "name": parts[0],
            "dsn": self._extract(line, r"DSN=([^,\s]+)"),
            "disp": self._extract(line, r"DISP=([^,]+)"),
            "type": self._dd_type(line),
            "raw": line
        }

    def _dd_type(self, line: str) -> str:
        if "SYSOUT=" in line:
            return "SYSOUT"
        if "DUMMY" in line:
            return "DUMMY"
        if "DSN=" in line:
            return "DATASET"
        if " DD *" in line:
            return "INLINE"
        return "UNKNOWN"

    def _extract(self, line: str, pattern: str) -> Optional[str]:
        m = re.search(pattern, line)
        return m.group(1) if m else None

    def _validate(self):
        if not self.ir["job"]:
            self.ir["warnings"].append("No JOB card found")

        if not self.ir["steps"]:
            raise ValueError("No EXEC steps found in JCL")
