"""Scoring and maintenance decision helpers."""

from __future__ import annotations

import pandas as pd

from pdm_toolkit.config import DEFAULT_RISK_THRESHOLDS


def assign_risk_tier(predicted_rul: float, thresholds: dict[str, int] | None = None) -> str:
    """Map predicted RUL to an operational risk tier."""
    thresholds = thresholds or DEFAULT_RISK_THRESHOLDS
    if predicted_rul <= thresholds["high"]:
        return "high"
    if predicted_rul <= thresholds["medium"]:
        return "medium"
    return "low"


def recommended_action(risk_tier: str) -> str:
    """Translate risk tier into a maintenance planning action."""
    return {
        "high": "Plan intervention in next maintenance window",
        "medium": "Inspect and monitor trend weekly",
        "low": "Continue routine monitoring",
    }[risk_tier]


def add_operational_recommendations(frame: pd.DataFrame) -> pd.DataFrame:
    """Add risk tier and action columns to scored assets."""
    scored = frame.copy()
    scored["failure_risk"] = scored["predicted_rul"].apply(assign_risk_tier)
    scored["maintenance_action"] = scored["failure_risk"].apply(recommended_action)
    return scored
