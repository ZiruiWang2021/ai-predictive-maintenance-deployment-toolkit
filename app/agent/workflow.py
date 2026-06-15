"""Practical ReACT-style agent workflow for predictive maintenance diagnosis."""

from __future__ import annotations

from typing import Any

from app.agent.schemas import AgentRunRequest, AgentRunResponse, AgentTraceStep
from app.agent.tools import (
    analyse_sensor_data,
    classify_risk,
    generate_maintenance_report,
    predict_rul,
    retrieve_manual_knowledge,
)


REACT_AGENT_PROMPT_TEMPLATE = """You are a predictive maintenance diagnosis agent.

Use this ReACT-style pattern:
- Reasoning: interpret the task and decide what information is needed.
- Action: call one available tool at a time.
- Observation: record the result from that tool.
- Final answer: combine evidence, RUL, risk, and limitations into a maintenance recommendation.

Available tools:
1. retrieve_manual_knowledge(question)
2. analyse_sensor_data(sensor_readings)
3. predict_rul(asset_id, sensor_readings)
4. classify_risk(rul, sensor_analysis, fault_description)
5. generate_maintenance_report(...)
"""


MAINTENANCE_REPORT_PROMPT_TEMPLATE = """Write a maintenance recommendation with:
- task interpretation,
- tools used,
- retrieved evidence,
- RUL estimate when available,
- risk level and explanation,
- recommended next action,
- limitations and uncertainty."""


def interpret_task(request: AgentRunRequest) -> str:
    """Create a concise task interpretation for the response."""
    fault = f" Observed fault: {request.fault_description}" if request.fault_description else ""
    sensor_state = "Sensor readings supplied." if request.sensor_readings else "No sensor readings supplied."
    return f"Assess asset {request.asset_id} for: {request.user_task}.{fault} {sensor_state}"


def should_retrieve_manual(request: AgentRunRequest) -> bool:
    """Decide whether manual knowledge is useful."""
    task_text = f"{request.user_task} {request.fault_description or ''}".lower()
    keywords = ["fault", "diagnos", "maintenance", "check", "inspect", "temperature", "bearing", "sensor", "overheat"]
    return bool(request.fault_description) or any(keyword in task_text for keyword in keywords)


def run_agent(request: AgentRunRequest) -> AgentRunResponse:
    """Run a deterministic ReACT-style maintenance diagnosis workflow.

    This maps to ReACT without an external orchestration service:
    - reasoning: each step explains why a tool is selected;
    - action: each selected function is called explicitly;
    - observation: the tool result is summarized and stored;
    - final answer: the maintenance report combines all observations.
    """
    trace: list[AgentTraceStep] = []
    tools_used: list[str] = []
    task_interpretation = interpret_task(request)

    trace.append(
        AgentTraceStep(
            reasoning="Interpret the user task and decide which diagnostic signals are available.",
            action="interpret_task",
            observation=task_interpretation,
        )
    )

    manual_answer: dict[str, Any] | None = None
    evidence: list[dict[str, Any]] = []
    if should_retrieve_manual(request):
        question = f"{request.user_task}. {request.fault_description or ''}".strip()
        tools_used.append("retrieve_manual_knowledge")
        manual_answer = retrieve_manual_knowledge(question)
        evidence = list(manual_answer.get("supporting_evidence", []))
        trace.append(
            AgentTraceStep(
                reasoning="Manual or fault context is needed, so retrieve relevant maintenance knowledge.",
                action="retrieve_manual_knowledge(question)",
                observation=f"Retrieved {len(evidence)} evidence snippet(s).",
            )
        )

    sensor_analysis = None
    if request.sensor_readings:
        tools_used.append("analyse_sensor_data")
        sensor_analysis = analyse_sensor_data(request.sensor_readings)
        trace.append(
            AgentTraceStep(
                reasoning="Sensor readings are available, so check for abnormal values before risk classification.",
                action="analyse_sensor_data(sensor_readings)",
                observation=sensor_analysis.summary,
            )
        )

    rul_estimate = None
    if request.sensor_readings:
        tools_used.append("predict_rul")
        rul_estimate = predict_rul(request.asset_id, request.sensor_readings)
        trace.append(
            AgentTraceStep(
                reasoning="Sensor readings are available, so estimate RUL using the existing predictive maintenance model.",
                action="predict_rul(asset_id, sensor_readings)",
                observation=f"Predicted RUL is {rul_estimate.predicted_rul:.1f} cycles.",
            )
        )

    tools_used.append("classify_risk")
    risk = classify_risk(
        rul=rul_estimate.predicted_rul if rul_estimate else None,
        sensor_analysis=sensor_analysis,
        fault_description=request.fault_description,
    )
    trace.append(
        AgentTraceStep(
            reasoning="Combine RUL, sensor analysis, and fault description to assign an operational risk tier.",
            action="classify_risk(rul, sensor_analysis, fault_description)",
            observation=f"Risk classified as {risk.risk_level}: {risk.explanation}",
        )
    )

    tools_used.append("generate_maintenance_report")
    report = generate_maintenance_report(
        asset_id=request.asset_id,
        user_task=request.user_task,
        risk=risk,
        sensor_analysis=sensor_analysis,
        rul_estimate=rul_estimate,
        evidence=evidence,
    )
    trace.append(
        AgentTraceStep(
            reasoning="Create the final answer from tool observations, evidence, and limitations.",
            action="generate_maintenance_report(...)",
            observation=report.recommended_next_action,
        )
    )

    limitations = list(report.limitations)
    if manual_answer:
        limitations.append(str(manual_answer.get("uncertainty_note", "")))
    elif not evidence:
        limitations.append("Manual retrieval was skipped because the task did not require document context.")

    return AgentRunResponse(
        task_interpretation=task_interpretation,
        tools_used=tools_used,
        react_trace=trace,
        evidence_retrieved=evidence,
        rul_estimate=rul_estimate,
        sensor_analysis=sensor_analysis,
        risk_level=risk.risk_level,
        risk_explanation=risk.explanation,
        recommended_next_action=report.recommended_next_action,
        maintenance_report=report,
        limitations=limitations,
        prompt_template=REACT_AGENT_PROMPT_TEMPLATE + "\n" + MAINTENANCE_REPORT_PROMPT_TEMPLATE,
    )
