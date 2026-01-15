import pytest
from backend.app.parsers.regex_parser.cobol_regex_parser import CobolRegexParser



@pytest.fixture
def parser():
    return CobolRegexParser()


@pytest.fixture
def sample_cobol_code():
    return """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLO-WORLD.

       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 NUM1 PIC 9(2).
       01 NUM2 PIC 9(2).
       01 RESULT PIC 9(3).

       PROCEDURE DIVISION.
       MAIN-PARA.
           DISPLAY "HELLO".
           ACCEPT NUM1.
           MOVE NUM1 TO NUM2.
           COMPUTE RESULT = NUM1 + NUM2.
           ADD NUM1 NUM2 GIVING RESULT.
           MULTIPLY NUM1 BY NUM2 GIVING RESULT.
           IF NUM1 > NUM2
               DISPLAY "NUM1 GREATER"
           END-IF.
           PERFORM CALC-PARA.
           STOP RUN.

       CALC-PARA.
           DISPLAY RESULT.
    """


# ==========================================================
# BASIC PARSING
# ==========================================================

def test_program_id_extraction(parser, sample_cobol_code):
    ir = parser.parse(sample_cobol_code)
    assert ir["program_info"]["program_id"] == "HELLO-WORLD"


def test_division_detection(parser, sample_cobol_code):
    ir = parser.parse(sample_cobol_code)
    assert ir["divisions"]["identification_division"] is True
    assert ir["divisions"]["data_division"] is True
    assert ir["divisions"]["procedure_division"] is True


# ==========================================================
# VARIABLES
# ==========================================================

def test_variable_extraction(parser, sample_cobol_code):
    ir = parser.parse(sample_cobol_code)

    var_names = {v["name"] for v in ir["variables"]}
    assert "NUM1" in var_names
    assert "NUM2" in var_names
    assert "RESULT" in var_names


# ==========================================================
# PARAGRAPHS
# ==========================================================

def test_paragraph_detection(parser, sample_cobol_code):
    ir = parser.parse(sample_cobol_code)

    para_names = {p["name"] for p in ir["paragraphs"]}
    assert "MAIN-PARA" in para_names
    assert "CALC-PARA" in para_names


# ==========================================================
# STATEMENTS
# ==========================================================

def test_statement_extraction(parser, sample_cobol_code):
    ir = parser.parse(sample_cobol_code)

    stmt_types = {s["type"] for s in ir["statements"]}

    assert "DISPLAY" in stmt_types
    assert "ACCEPT" in stmt_types
    assert "MOVE" in stmt_types
    assert "COMPUTE" in stmt_types
    assert "ADD" in stmt_types
    assert "MULTIPLY" in stmt_types
    assert "STOP" in stmt_types


# ==========================================================
# CONTROL FLOW
# ==========================================================

def test_control_flow_extraction(parser, sample_cobol_code):
    ir = parser.parse(sample_cobol_code)

    cf_types = {c["type"] for c in ir["control_flow"]}

    assert "IF" in cf_types
    assert "PERFORM" in cf_types


def test_if_condition_capture(parser, sample_cobol_code):
    ir = parser.parse(sample_cobol_code)
    assert any("NUM1 > NUM2" in cond for cond in ir["conditions"])


# ==========================================================
# PERFORM CALL GRAPH
# ==========================================================

def test_perform_extraction(parser, sample_cobol_code):
    ir = parser.parse(sample_cobol_code)

    targets = {p["target"] for p in ir["performs"]}
    assert "CALC-PARA" in targets


# ==========================================================
# FILE OPERATIONS
# ==========================================================

def test_file_operation_detection(parser):
    cobol = """
       PROCEDURE DIVISION.
           OPEN INPUT MYFILE.
           READ MYFILE.
           CLOSE MYFILE.
           STOP RUN.
    """

    ir = parser.parse(cobol)
    ops = {f["operation"] for f in ir["file_operations"]}

    assert "OPEN" in ops
    assert "READ" in ops
    assert "CLOSE" in ops


# ==========================================================
# WARNINGS
# ==========================================================

def test_warning_when_no_executable_logic(parser):
    cobol = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. EMPTYPROG.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 A PIC 9.
    """

    ir = parser.parse(cobol)
    assert len(ir["warnings"]) == 1
    assert "No executable logic detected" in ir["warnings"][0]
