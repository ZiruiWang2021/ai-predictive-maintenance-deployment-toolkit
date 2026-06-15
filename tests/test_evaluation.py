"""Smoke tests for the lightweight evaluation module."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.evaluation.evaluate_agent import evaluate_case as evaluate_agent_case  # noqa: E402
from app.evaluation.evaluate_rag import evaluate_case as evaluate_rag_case  # noqa: E402
from app.evaluation.evaluate_rag import load_test_cases  # noqa: E402


class EvaluationTests(unittest.TestCase):
    def test_test_question_file_contains_twenty_cases(self) -> None:
        cases = load_test_cases()
        self.assertEqual(len(cases), 20)
        self.assertTrue(all("question" in case for case in cases))
        self.assertTrue(all("agent_request" in case for case in cases))

    def test_rag_evaluation_case_returns_expected_checks(self) -> None:
        case = load_test_cases()[0]
        result = evaluate_rag_case(case)
        self.assertIn("has_sources", result)
        self.assertIn("has_context", result)
        self.assertIn("uncertainty_ok", result)

    def test_agent_evaluation_case_returns_expected_checks(self) -> None:
        case = load_test_cases()[0]
        result = evaluate_agent_case(case)
        self.assertIn("risk_level_valid", result)
        self.assertIn("tools_relevant", result)
        self.assertIn("has_next_action", result)


if __name__ == "__main__":
    unittest.main()
