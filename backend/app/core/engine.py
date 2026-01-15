from backend.app.core.parser_factory import get_parser
from backend.app.llm.explainer import explain
from backend.app.analyzers.summarizer import summarize


def run_pipeline(code: str, language: str = "cobol") -> dict:
    language = language.lower()

    parser = get_parser(language)
    ir = parser.parse(code)

    analysis = {}
    if language == "cobol":
        analysis = summarize(ir)

    explanation = explain(ir, language)

    return {
        "language": language,
        "intermediate_representation": ir,
        "analysis": analysis,
        "explanation": explanation
    }
