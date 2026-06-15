"""Lightweight RAG evaluation for predictive maintenance questions.

This evaluator checks observable response fields instead of trying to grade
answer quality with another model. That makes the results easy to explain and
reproduce in a portfolio or interview setting.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.rag.retriever import generate_rag_answer, retrieve_context  # noqa: E402


TEST_QUESTIONS_PATH = Path(__file__).with_name("test_questions.json")
DEFAULT_OUTPUT_PATH = Path(__file__).with_name("evaluation_results.json")
UNCERTAINTY_TERMS = ("limited", "weak", "insufficient", "not enough", "verify", "uncertain")


def load_test_cases(path: Path = TEST_QUESTIONS_PATH) -> list[dict[str, Any]]:
    """Load synthetic evaluation cases from JSON."""
    return json.loads(path.read_text(encoding="utf-8"))


def contains_uncertainty_note(text: str) -> bool:
    """Return True when a response clearly admits uncertainty or weak evidence."""
    lowered = text.lower()
    return any(term in lowered for term in UNCERTAINTY_TERMS)


def evaluate_case(case: dict[str, Any], top_k: int = 4) -> dict[str, Any]:
    """Evaluate one RAG answer using transparent boolean checks."""
    question = str(case["question"])
    contexts = retrieve_context(question, top_k=top_k)
    answer = generate_rag_answer(question, top_k=top_k)

    source_documents = answer.get("source_documents", [])
    supporting_evidence = answer.get("supporting_evidence", [])
    expected_sources = set(case.get("expected_rag_sources", []))
    observed_sources = set(source_documents)
    requires_uncertainty = bool(case.get("requires_uncertainty", False))

    has_source_documents = bool(source_documents)
    retrieved_context_non_empty = bool(contexts) and bool(supporting_evidence)
    expected_source_hit = not expected_sources or bool(expected_sources.intersection(observed_sources))
    uncertainty_ok = (
        contains_uncertainty_note(str(answer.get("uncertainty_note", "")))
        if requires_uncertainty
        else True
    )

    passed = all([has_source_documents, retrieved_context_non_empty, expected_source_hit, uncertainty_ok])
    return {
        "id": case["id"],
        "has_sources": has_source_documents,
        "has_context": retrieved_context_non_empty,
        "expected_source_hit": expected_source_hit,
        "uncertainty_ok": uncertainty_ok,
        "passed": passed,
        "source_documents": source_documents,
        "uncertainty_note": answer.get("uncertainty_note", ""),
    }


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(1 for result in results if result["passed"])
    total = len(results)
    return {"total": total, "passed": passed, "failed": total - passed, "pass_rate": round(passed / total, 3) if total else 0.0}


def format_bool(value: bool) -> str:
    return "PASS" if value else "FAIL"


def print_table(results: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    rows = [
        {
            "id": result["id"],
            "sources": format_bool(result["has_sources"]),
            "context": format_bool(result["has_context"]),
            "source_hit": format_bool(result["expected_source_hit"]),
            "uncertainty": format_bool(result["uncertainty_ok"]),
            "overall": format_bool(result["passed"]),
        }
        for result in results
    ]
    columns = ["id", "sources", "context", "source_hit", "uncertainty", "overall"]
    widths = {column: max(len(column), *(len(str(row[column])) for row in rows)) for column in columns}
    header = " | ".join(column.ljust(widths[column]) for column in columns)
    rule = "-+-".join("-" * widths[column] for column in columns)
    print(header)
    print(rule)
    for row in rows:
        print(" | ".join(str(row[column]).ljust(widths[column]) for column in columns))
    print()
    print(f"RAG evaluation: {summary['passed']}/{summary['total']} passed (pass rate {summary['pass_rate']:.1%}).")


def save_results(results: list[dict[str, Any]], summary: dict[str, Any], output_path: Path) -> None:
    payload = {"suite": "rag", "summary": summary, "results": results}
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Saved results to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate RAG outputs with transparent field checks.")
    parser.add_argument("--questions", type=Path, default=TEST_QUESTIONS_PATH, help="Path to test questions JSON.")
    parser.add_argument("--top-k", type=int, default=4, help="Number of chunks to retrieve per question.")
    parser.add_argument("--save", action="store_true", help="Save results to JSON.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH, help="Output JSON path when --save is used.")
    args = parser.parse_args()

    cases = load_test_cases(args.questions)
    results = [evaluate_case(case, top_k=args.top_k) for case in cases]
    summary = summarize(results)
    print_table(results, summary)
    if args.save:
        save_results(results, summary, args.output)


if __name__ == "__main__":
    main()
