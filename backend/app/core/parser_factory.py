from backend.app.parsers.regex_parser.cobol_regex_parser import CobolRegexParser
from backend.app.parsers.jcl_parser.parser import JCLParser


def get_parser(language: str = "cobol"):
    language = language.lower()

    if language == "cobol":
        return CobolRegexParser()

    if language == "jcl":
        return JCLParser()

    raise ValueError(f"Unsupported language: {language}")

