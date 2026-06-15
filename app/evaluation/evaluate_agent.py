"""Lightweight evaluation for the predictive maintenance Agent workflow."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.agent.schemas import AgentRunRequest  # noqa: E402
from app.agent.workflow import run_agent  # noqa: E402


TEST_QUESTIONS_PATH = Path(__file__).with_name("test_questions.json")
DEFAULT_OUTPUT_PATH = Path(__file__).with_name("evaluation_results.json")
VALID_RISK_LEVELS = {"Low", "Medium", "High", "Unknown"}
UNCERTAINTY_TERMS = ("limited", "weak", "insufficient", "not enough", "verify", "uncertain", "skipped")


def load_test_cases(path: Path = TEST_QUESTIONS_PATH) -> list[dict[str, Any]]:
    """Load synthetic evaluation cases from JSON."""
    return json.loads(path.read_text(encoding="utf-8"))


def contains_uncertainty_note(values: list[str]) -> bool:
    """Return True when limitations admit uncertainty or missing evidence."""
    text = " ".join(values).lower()
    return any(term in text for term in UNCERTAINTY_TERMS)


def evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    """Evaluate one Agent response using transparent boolean checks."""
    request = AgentRunRequest(**case["agent_request"])
    response = run_agent(request)

    expected_tools = set(case.get("expected_tools", []))
    observed_tools = set(response.tools_used)
    requires_retrieval = "retrieve_manual_knowledge" in expected_tools
    requires_uncertainty = bool(case.get("requires_uncertainty", False))

    has_source_documents = (not requires_retrieval) or bool(response.evidence_retrieved)
    retrieved_context_non_empty = (not requires_retrieval) or bool(response.evidence_retrieved)
    risk_level_valid = response.risk_level in VALID_RISK_LEVELS
    selected_relevant_tools = expected_tools.issubset(observed_tools)
    has_recommended_next_action = bool(response.recommended_next_action.strip())
    uncertainty_ok = contains_uncertainty_note(response.limitations) if requires_uncertainty else True

    passed = all([
        has_source_documents,
        retrieved_context_non_empty,
        risk_level_valid,
        selected_relevant_tools,
        has_recommended_next_action,
        uncertainty_ok,
    ])
    return {
        "id": case["id"],
        "has_sources": has_source_documents,
        "has_context": retrieved_context_non_empty,
        "risk_level_valid": risk_level_valid,
        "tools_relevant": selected_relevant_tools,
        "has_next_action": has_recommended_next_action,
        "uncertainty_ok": uncertainty_ok,
        "passed": passed,
        "risk_level": response.risk_level,
        "tools_used": response.tools_used,
        "recommended_next_action": response.recommended_next_action,
        "limitations": response.limitations,
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
            "risk": format_bool(result["risk_level_valid"]),
            "tools": format_bool(result["tools_relevant"]),
            "action": format_bool(result["has_next_action"]),
            "uncertainty": format_bool(result["uncertainty_ok"]),
            "overall": format_bool(result["passed"]),
        }
        for result in results
    ]
    columns = ["id", "sources", "context", "risk", "tools", "action", "uncertainty", "overall"]
    widths = {column: max(len(column), *(len(str(row[column])) for row in rows)) for column in columns}
    header = " | ".join(column.ljust(widths[column]) for column in columns)
    rule = "-+-".join("-" * widths[column] for column in columns)
    print(header)
    print(rule)
    for row in rows:
        print(" | ".join(str(row[column]).ljust(widths[column]) for column in columns))
    print()
    print(f"Agent evaluation: {summary['passed']}/{summary['total']} passed (pass rate {summary['pass_rate']:.1%}).")


def save_results(results: list[dict[str, Any]], summary: dict[str, Any], output_path: Path) -> None:
    payload = {"suite": "agent", "summary": summary, "results": results}
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Saved results to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate Agent outputs with transparent field checks.")
    parser.add_argument("--questions", type=Path, default=TEST_QUESTIONS_PATH, help="Path to test questions JSON.")
    parser.add_argument("--save", action="store_true", help="Save results to JSON.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH, help="Output JSON path when --save is used.")
    args = parser.parse_args()

    cases = load_test_cases(args.questions)
    results = [evaluate_case(case) for case in cases]
    summary = summarize(results)
    print_table(results, summary)
    if args.save:
        save_results(results, summary, args.output)


if __name__ == "__main__":
    main()
