"""Pydantic schemas for the predictive maintenance agent."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


RiskLevel = Literal["Low", "Medium", "High", "Unknown"]


class AgentRunRequest(BaseModel):
    """Request body for the agent workflow."""

    asset_id: int = Field(..., description="Asset identifier used for RUL prediction and reporting.")
    user_task: str = Field(..., min_length=3, description="Natural language task for the maintenance agent.")
    fault_description: str | None = Field(None, description="Optional observed fault or symptom description.")
    sensor_readings: dict[str, Any] | None = Field(
        None,
        description="Optional sensor values. Supports sensor_01..sensor_12 plus friendly keys such as temperature.",
    )


class EvidenceSnippet(BaseModel):
    """Retrieved manual evidence used by the agent."""

    source: str
    chunk_id: str
    score: float
    text: str


class SensorAnalysis(BaseModel):
    """Summary of sensor abnormality checks."""

    summary: str
    abnormal_values: list[str]
    severity_hint: RiskLevel
    data_quality_notes: list[str]


class RULEstimate(BaseModel):
    """RUL prediction output from the existing predictive maintenance model."""

    predicted_rul: float
    prediction_interval_low: float
    prediction_interval_high: float
    model_source: str
    notes: list[str]


class RiskClassification(BaseModel):
    """Risk classification with reasoning."""

    risk_level: RiskLevel
    explanation: str


class AgentTraceStep(BaseModel):
    """One ReACT-style reasoning/action/observation step."""

    reasoning: str
    action: str
    observation: str


class MaintenanceReport(BaseModel):
    """Final structured maintenance recommendation."""

    recommended_next_action: str
    rationale: list[str]
    limitations: list[str]


class AgentRunResponse(BaseModel):
    """Response body returned by POST /agent/run."""

    task_interpretation: str
    tools_used: list[str]
    react_trace: list[AgentTraceStep]
    evidence_retrieved: list[EvidenceSnippet]
    rul_estimate: RULEstimate | None
    sensor_analysis: SensorAnalysis | None
    risk_level: RiskLevel
    risk_explanation: str
    recommended_next_action: str
    maintenance_report: MaintenanceReport
    limitations: list[str]
    prompt_template: str
