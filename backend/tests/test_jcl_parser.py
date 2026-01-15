import pytest

from backend.app.parsers.jcl_parser.parser import JCLParser


@pytest.fixture
def sample_jcl():
    return """//MYJOB01 JOB (1234),CLASS=A,MSGCLASS=H,NOTIFY=USER01
//STEP1   EXEC PGM=IEFBR14
//DD1     DD DSN=TEST.DATA.SET,DISP=SHR
//DD2     DD SYSOUT=*
//STEP2   EXEC PROC=CLEANUP
//DD3     DD DUMMY
"""


def test_jcl_parser_basic_structure(sample_jcl):
    parser = JCLParser()
    ir = parser.parse(sample_jcl)

    assert "job" in ir
    assert "steps" in ir
    assert "datasets" in ir
    assert "warnings" in ir


def test_job_card_parsed_correctly(sample_jcl):
    parser = JCLParser()
    ir = parser.parse(sample_jcl)

    job = ir["job"]
    assert job["name"] == "MYJOB01"
    assert job["class"] == "A"
    assert job["msgclass"] == "H"
    assert job["notify"] == "USER01"


def test_exec_steps_detected(sample_jcl):
    parser = JCLParser()
    ir = parser.parse(sample_jcl)

    steps = ir["steps"]
    assert len(steps) == 2

    assert steps[0]["name"] == "STEP1"
    assert steps[0]["program"] == "IEFBR14"

    assert steps[1]["name"] == "STEP2"
    assert steps[1]["procedure"] == "CLEANUP"


def test_dd_statements_attached_to_steps(sample_jcl):
    parser = JCLParser()
    ir = parser.parse(sample_jcl)

    step1_dds = ir["steps"][0]["dds"]
    step2_dds = ir["steps"][1]["dds"]

    assert len(step1_dds) == 2
    assert step1_dds[0]["dsn"] == "TEST.DATA.SET"
    assert step1_dds[0]["type"] == "DATASET"
    assert step1_dds[1]["type"] == "SYSOUT"

    assert len(step2_dds) == 1
    assert step2_dds[0]["type"] == "DUMMY"


def test_datasets_collected(sample_jcl):
    parser = JCLParser()
    ir = parser.parse(sample_jcl)

    assert "TEST.DATA.SET" in ir["datasets"]


def test_get_ir_returns_same_ir(sample_jcl):
    parser = JCLParser()
    parser.parse(sample_jcl)

    ir = parser.get_ir()
    assert isinstance(ir, dict)
    assert "steps" in ir


def test_missing_job_card_adds_warning():
    jcl = """//STEP1 EXEC PGM=IEFBR14"""

    parser = JCLParser()
    ir = parser.parse(jcl)

    assert "No JOB card found" in ir["warnings"]


def test_no_exec_steps_raises_error():
    jcl = """//MYJOB01 JOB CLASS=A"""

    parser = JCLParser()

    with pytest.raises(ValueError) as exc:
        parser.parse(jcl)

    assert "No EXEC steps found in JCL" in str(exc.value)
