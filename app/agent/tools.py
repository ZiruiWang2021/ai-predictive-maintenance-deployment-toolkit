"""Tool functions used by the predictive maintenance agent."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

import pandas as pd

from app.agent.schemas import MaintenanceReport, RULEstimate, RiskClassification, SensorAnalysis
from app.rag.retriever import generate_rag_answer


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from pdm_toolkit.config import SENSOR_COLUMNS, SETTING_COLUMNS  # noqa: E402
from pdm_toolkit.features import align_features, build_feature_table  # noqa: E402
from pdm_toolkit.model import load_model  # noqa: E402
from pdm_toolkit.pipeline import build_demo_artifacts  # noqa: E402


MODEL_PATH = PROJECT_ROOT / "artifacts" / "rul_ridge_model.pkl"

DEFAULT_SENSOR_VALUES = {
    "sensor_01": 640.0,
    "sensor_02": 1585.0,
    "sensor_03": 1400.0,
    "sensor_04": 14.5,
    "sensor_05": 21.6,
    "sensor_06": 554.0,
    "sensor_07": 2388.0,
    "sensor_08": 9050.0,
    "sensor_09": 1.3,
    "sensor_10": 47.0,
    "sensor_11": 520.0,
    "sensor_12": 39.0,
}

FRIENDLY_SENSOR_MAP = {
    "temperature": "sensor_05",
    "motor_temperature": "sensor_05",
    "bearing_temperature": "sensor_05",
    "vibration": "sensor_09",
    "current": "sensor_10",
    "airflow": "sensor_06",
    "pressure": "sensor_02",
}


def _numeric(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def retrieve_manual_knowledge(question: str) -> dict[str, Any]:
    """Retrieve maintenance manual knowledge through the existing RAG retriever."""
    return generate_rag_answer(question)


def analyse_sensor_data(sensor_readings: dict[str, Any] | None) -> SensorAnalysis:
    """Return a short heuristic analysis of abnormal sensor values."""
    if not sensor_readings:
        return SensorAnalysis(
            summary="No sensor readings were supplied, so sensor abnormality analysis was skipped.",
            abnormal_values=[],
            severity_hint="Unknown",
            data_quality_notes=["Sensor readings are required for trend or threshold-based diagnosis."],
        )

    abnormal_values: list[str] = []
    notes: list[str] = []

    for key, raw_value in sorted(sensor_readings.items()):
        value = _numeric(raw_value)
        if value is None:
            if key not in {"asset_class", "failure_mode"}:
                notes.append(f"{key} is non-numeric and was not used for threshold analysis.")
            continue

        lowered = key.lower()
        if "temp" in lowered or "temperature" in lowered:
            if value >= 85:
                abnormal_values.append(f"{key}={value:g} is high for a temperature signal.")
            elif value >= 75:
                abnormal_values.append(f"{key}={value:g} is elevated for a temperature signal.")
        elif "vibration" in lowered:
            if value >= 7:
                abnormal_values.append(f"{key}={value:g} is high vibration.")
            elif value >= 4:
                abnormal_values.append(f"{key}={value:g} is elevated vibration.")
        elif "current" in lowered:
            if value >= 120:
                abnormal_values.append(f"{key}={value:g} suggests high current or overload.")
        elif key in SENSOR_COLUMNS:
            baseline = DEFAULT_SENSOR_VALUES[key]
            if baseline and abs(value - baseline) / abs(baseline) >= 0.25:
                abnormal_values.append(f"{key}={value:g} deviates more than 25% from the demo baseline {baseline:g}.")

    if not abnormal_values:
        severity = "Low"
        summary = "No obvious abnormal sensor values were detected by the local heuristic checks."
    elif len(abnormal_values) >= 3:
        severity = "High"
        summary = "Multiple abnormal sensor values were detected and should be reviewed together."
    else:
        severity = "Medium"
        summary = "One or two abnormal sensor values were detected and should be validated against manual guidance."

    if "cycle" not in sensor_readings:
        notes.append("No cycle value supplied; prediction will use a default current cycle.")

    return SensorAnalysis(
        summary=summary,
        abnormal_values=abnormal_values,
        severity_hint=severity,  # type: ignore[arg-type]
        data_quality_notes=notes,
    )


def _build_prediction_row(asset_id: int, sensor_readings: dict[str, Any] | None) -> pd.DataFrame:
    readings = sensor_readings or {}
    row: dict[str, Any] = {
        "unit_id": int(asset_id),
        "cycle": int(_numeric(readings.get("cycle")) or 100),
        "asset_class": str(readings.get("asset_class", "standard")),
        "failure_mode": str(readings.get("failure_mode", "unknown")),
    }
    for setting in SETTING_COLUMNS:
        row[setting] = float(_numeric(readings.get(setting)) or 0.0)

    sensor_values = DEFAULT_SENSOR_VALUES.copy()
    for key, value in readings.items():
        target_key = FRIENDLY_SENSOR_MAP.get(key.lower(), key)
        if target_key in SENSOR_COLUMNS:
            numeric_value = _numeric(value)
            if numeric_value is not None:
                sensor_values[target_key] = numeric_value
    row.update(sensor_values)
    return pd.DataFrame([row])


def predict_rul(asset_id: int, sensor_readings: dict[str, Any] | None) -> RULEstimate:
    """Predict RUL with the existing ridge RUL model."""
    notes: list[str] = []
    if not MODEL_PATH.exists():
        build_demo_artifacts(PROJECT_ROOT, n_units=60)
        notes.append("Model artifact was missing, so demo artifacts were generated locally before prediction.")

    model = load_model(MODEL_PATH)
    feature_frame = build_feature_table(_build_prediction_row(asset_id, sensor_readings))
    features = align_features(feature_frame, model.feature_columns)
    prediction = model.predict(features)
    low, high = model.prediction_interval(prediction)
    notes.append("Single-row prediction uses supplied readings plus demo defaults for missing sensors.")
    return RULEstimate(
        predicted_rul=round(float(prediction[0]), 2),
        prediction_interval_low=round(float(low[0]), 2),
        prediction_interval_high=round(float(high[0]), 2),
        model_source="artifacts/rul_ridge_model.pkl",
        notes=notes,
    )


def classify_risk(
    rul: float | None,
    sensor_analysis: SensorAnalysis | None,
    fault_description: str | None,
) -> RiskClassification:
    """Classify maintenance risk from RUL, sensor abnormalities, and fault text."""
    fault_text = (fault_description or "").lower()
    severity_hint = sensor_analysis.severity_hint if sensor_analysis else "Unknown"
    abnormal_count = len(sensor_analysis.abnormal_values) if sensor_analysis else 0

    reasons: list[str] = []
    if rul is not None:
        reasons.append(f"Predicted RUL is {rul:.1f} cycles.")
    if abnormal_count:
        reasons.append(f"Sensor analysis found {abnormal_count} abnormal value(s).")
    if fault_description:
        reasons.append(f"Fault description mentions: {fault_description}.")

    high_fault_terms = ["overheat", "overheating", "bearing", "vibration", "alarm", "thermal"]
    medium_fault_terms = ["noise", "trend", "inspect", "anomaly", "sensor"]

    if (rul is not None and rul <= 30) or severity_hint == "High" or any(term in fault_text for term in high_fault_terms):
        level = "High"
    elif (rul is not None and rul <= 60) or severity_hint == "Medium" or any(term in fault_text for term in medium_fault_terms):
        level = "Medium"
    elif rul is None and severity_hint == "Unknown" and not fault_description:
        level = "Unknown"
    else:
        level = "Low"

    explanation = " ".join(reasons) if reasons else "Insufficient evidence was supplied for confident risk classification."
    return RiskClassification(risk_level=level, explanation=explanation)  # type: ignore[arg-type]


def generate_maintenance_report(
    asset_id: int,
    user_task: str,
    risk: RiskClassification,
    sensor_analysis: SensorAnalysis | None,
    rul_estimate: RULEstimate | None,
    evidence: list[dict[str, Any]],
) -> MaintenanceReport:
    """Produce a structured maintenance recommendation."""
    if risk.risk_level == "High":
        action = "Plan inspection or intervention in the next safe maintenance window."
    elif risk.risk_level == "Medium":
        action = "Inspect the asset, validate sensor signals, and monitor the trend more frequently."
    elif risk.risk_level == "Low":
        action = "Continue routine monitoring and keep the asset under normal maintenance cadence."
    else:
        action = "Collect sensor readings or fault details before making a maintenance decision."

    rationale = [f"Asset {asset_id}: {user_task}", risk.explanation]
    if rul_estimate:
        rationale.append(
            f"RUL estimate: {rul_estimate.predicted_rul:.1f} cycles "
            f"({rul_estimate.prediction_interval_low:.1f}-{rul_estimate.prediction_interval_high:.1f})."
        )
    if sensor_analysis and sensor_analysis.abnormal_values:
        rationale.extend(sensor_analysis.abnormal_values[:3])
    if evidence:
        rationale.append(
            "Manual evidence retrieved from: "
            + ", ".join(sorted({str(item["source"]) for item in evidence}))
            + "."
        )

    limitations = [
        "Agent output is decision support only and does not replace OEM manuals or safety procedures.",
        "RAG evidence comes from synthetic demo documents unless replaced with real manuals.",
    ]
    if not rul_estimate:
        limitations.append("RUL prediction was skipped because no sensor readings were supplied.")
    if sensor_analysis and sensor_analysis.data_quality_notes:
        limitations.extend(sensor_analysis.data_quality_notes)

    return MaintenanceReport(recommended_next_action=action, rationale=rationale, limitations=limitations)
