"""Streamlit dashboard for the predictive maintenance demo."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))


@st.cache_data(show_spinner=False)
def load_outputs() -> tuple[pd.DataFrame, pd.DataFrame, dict[str, float]]:
    fleet_path = PROJECT_ROOT / "data" / "processed" / "fleet_latest_predictions.csv"
    eval_path = PROJECT_ROOT / "data" / "processed" / "evaluation_predictions.csv"
    metrics_path = PROJECT_ROOT / "artifacts" / "model_metrics.json"
    missing = [path for path in [fleet_path, eval_path, metrics_path] if not path.exists()]
    if missing:
        names = ", ".join(str(path.relative_to(PROJECT_ROOT)) for path in missing)
        raise FileNotFoundError(f"Missing generated artifacts: {names}")
    fleet = pd.read_csv(fleet_path)
    evaluation = pd.read_csv(eval_path)
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    return fleet, evaluation, metrics


def risk_order(value: str) -> int:
    return {"high": 0, "medium": 1, "low": 2}.get(value, 3)


def format_metric(value: float) -> str:
    return f"{value:,.1f}"


st.set_page_config(page_title="Predictive Maintenance Toolkit", layout="wide")
st.title("AI Predictive Maintenance Deployment Toolkit")

try:
    fleet_df, eval_df, model_metrics = load_outputs()
except FileNotFoundError as exc:
    st.warning(str(exc))
    st.code("python scripts/train_model.py --generate-sample --n-units 90", language="bash")
    st.stop()

with st.sidebar:
    st.header("Filters")
    selected_risks = st.multiselect(
        "Failure risk",
        options=["high", "medium", "low"],
        default=["high", "medium", "low"],
    )
    max_rul = st.slider("Max predicted RUL", min_value=0, max_value=125, value=125, step=5)
    selected_unit = st.selectbox("Asset detail", options=sorted(fleet_df["unit_id"].unique()))

filtered = fleet_df[
    fleet_df["failure_risk"].isin(selected_risks) & (fleet_df["predicted_rul"] <= max_rul)
].copy()
filtered["risk_sort"] = filtered["failure_risk"].apply(risk_order)
filtered = filtered.sort_values(["risk_sort", "predicted_rul", "unit_id"])

high_risk_count = int((fleet_df["failure_risk"] == "high").sum())
medium_risk_count = int((fleet_df["failure_risk"] == "medium").sum())
median_rul = float(fleet_df["predicted_rul"].median())
recall = float(model_metrics["failure_horizon_recall"])

kpi_columns = st.columns(4)
kpi_columns[0].metric("Fleet assets", f"{len(fleet_df):,}")
kpi_columns[1].metric("High-risk assets", f"{high_risk_count:,}")
kpi_columns[2].metric("Median predicted RUL", format_metric(median_rul))
kpi_columns[3].metric("Failure horizon recall", f"{recall:.0%}")

left, right = st.columns([1.35, 1])

with left:
    st.subheader("Maintenance Intervention Queue")
    queue_columns = [
        "unit_id",
        "cycle",
        "predicted_rul",
        "prediction_interval_low",
        "prediction_interval_high",
        "failure_risk",
        "maintenance_action",
    ]
    st.dataframe(filtered[queue_columns].head(25), use_container_width=True, hide_index=True)

with right:
    st.subheader("Risk Mix")
    risk_mix = fleet_df["failure_risk"].value_counts().reindex(["high", "medium", "low"]).fillna(0)
    st.bar_chart(risk_mix)

st.subheader("Predicted RUL by Asset")
chart_data = filtered[["unit_id", "predicted_rul"]].set_index("unit_id").head(40)
st.bar_chart(chart_data)

detail_left, detail_right = st.columns([1, 1])

with detail_left:
    st.subheader("Selected Asset")
    asset_row = fleet_df[fleet_df["unit_id"] == selected_unit].iloc[0]
    st.write(
        {
            "unit_id": int(asset_row["unit_id"]),
            "latest_cycle": int(asset_row["cycle"]),
            "predicted_rul": float(asset_row["predicted_rul"]),
            "failure_risk": asset_row["failure_risk"],
            "recommended_action": asset_row["maintenance_action"],
        }
    )

with detail_right:
    st.subheader("Model Validation")
    validation_metrics = pd.DataFrame(
        [
            {"metric": "MAE", "value": model_metrics["mae"]},
            {"metric": "RMSE", "value": model_metrics["rmse"]},
            {"metric": "Bias", "value": model_metrics["bias"]},
            {"metric": "Within 20 cycles", "value": model_metrics["within_20_cycles_pct"]},
            {"metric": "Horizon precision", "value": model_metrics["failure_horizon_precision"]},
            {"metric": "Horizon recall", "value": model_metrics["failure_horizon_recall"]},
        ]
    )
    st.dataframe(validation_metrics, use_container_width=True, hide_index=True)

st.subheader("Evaluation Scatter")
scatter = eval_df[["rul", "predicted_rul"]].rename(columns={"rul": "actual_rul"})
st.scatter_chart(scatter, x="actual_rul", y="predicted_rul")

st.caption("Demo decision support only. Risk thresholds and maintenance actions require domain calibration before production use.")
