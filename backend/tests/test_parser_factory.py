import pytest

from backend.app.core.parser_factory import get_parser
from backend.app.parsers.regex_parser.cobol_regex_parser import CobolRegexParser
from backend.app.parsers.jcl_parser.parser import JCLParser


def test_get_parser_returns_cobol_parser():
    """
    Ensure COBOL language returns CobolRegexParser
    """
    parser = get_parser(language="cobol")
    assert isinstance(parser, CobolRegexParser)


def test_get_parser_returns_jcl_parser():
    """
    Ensure JCL language returns JCLParser
    """
    parser = get_parser(language="jcl")
    assert isinstance(parser, JCLParser)


def test_get_parser_language_case_insensitive():
    """
    Ensure language input is case-insensitive
    """
    parser = get_parser(language="COBOL")
    assert isinstance(parser, CobolRegexParser)

    parser = get_parser(language="JCL")
    assert isinstance(parser, JCLParser)


def test_get_parser_invalid_language_raises_error():
    """
    Ensure unsupported language raises ValueError
    """
    with pytest.raises(ValueError) as exc:
        get_parser(language="python")

    assert "Unsupported language" in str(exc.value)
