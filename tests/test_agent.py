"""Agent workflow tests."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.agent.schemas import AgentRunRequest
from app.agent.workflow import run_agent
from app.main import agent_run


class AgentWorkflowTests(unittest.TestCase):
    def sample_request(self) -> AgentRunRequest:
        return AgentRunRequest(
            asset_id=42,
            user_task="Diagnose abnormal motor temperature and recommend next action",
            fault_description="Motor temperature is rising and vibration alarm triggered.",
            sensor_readings={
                "cycle": 140,
                "temperature": 92,
                "vibration": 8.2,
                "current": 132,
                "asset_class": "route-critical",
            },
        )

    def test_agent_runs_all_required_tools_for_sensor_fault(self) -> None:
        response = run_agent(self.sample_request())
        self.assertIn("retrieve_manual_knowledge", response.tools_used)
        self.assertIn("analyse_sensor_data", response.tools_used)
        self.assertIn("predict_rul", response.tools_used)
        self.assertIn("classify_risk", response.tools_used)
        self.assertIn("generate_maintenance_report", response.tools_used)
        self.assertGreater(len(response.evidence_retrieved), 0)
        self.assertIsNotNone(response.rul_estimate)
        self.assertEqual(response.risk_level, "High")
        self.assertGreaterEqual(len(response.react_trace), 5)

    def test_agent_endpoint_returns_structured_response(self) -> None:
        response = agent_run(self.sample_request())
        payload = response.model_dump()
        self.assertEqual(payload["risk_level"], "High")
        self.assertIn("recommended_next_action", payload)
        self.assertIn("react_trace", payload)
        self.assertIn("prompt_template", payload)


if __name__ == "__main__":
    unittest.main()
