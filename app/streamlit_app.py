"""Streamlit dashboard for the predictive maintenance demo."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

RISK_LABELS = {
    "high": "高风险 / High",
    "medium": "中风险 / Medium",
    "low": "低风险 / Low",
}

ACTION_LABELS = {
    "Plan intervention in next maintenance window": "下个维护窗口安排干预 / Plan intervention in next maintenance window",
    "Inspect and monitor trend weekly": "每周检查并跟踪趋势 / Inspect and monitor trend weekly",
    "Continue routine monitoring": "继续常规监控 / Continue routine monitoring",
}


@st.cache_data(show_spinner=False)
def load_outputs() -> tuple[pd.DataFrame, pd.DataFrame, dict[str, float]]:
    fleet_path = PROJECT_ROOT / "data" / "processed" / "fleet_latest_predictions.csv"
    eval_path = PROJECT_ROOT / "data" / "processed" / "evaluation_predictions.csv"
    metrics_path = PROJECT_ROOT / "artifacts" / "model_metrics.json"
    missing = [path for path in [fleet_path, eval_path, metrics_path] if not path.exists()]
    if missing:
        names = ", ".join(str(path.relative_to(PROJECT_ROOT)) for path in missing)
        raise FileNotFoundError(f"缺少生成文件 / Missing generated artifacts: {names}")
    fleet = pd.read_csv(fleet_path)
    evaluation = pd.read_csv(eval_path)
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    return fleet, evaluation, metrics


def risk_order(value: str) -> int:
    return {"high": 0, "medium": 1, "low": 2}.get(value, 3)


def format_metric(value: float) -> str:
    return f"{value:,.1f}"


def bilingual_risk(value: str) -> str:
    return RISK_LABELS.get(value, value)


def bilingual_action(value: str) -> str:
    return ACTION_LABELS.get(value, value)


st.set_page_config(page_title="AI 预测性维护工具包 / Predictive Maintenance Toolkit", layout="wide")
st.title("AI 预测性维护部署工具包 / AI Predictive Maintenance Deployment Toolkit")

try:
    fleet_df, eval_df, model_metrics = load_outputs()
except FileNotFoundError as exc:
    st.warning(str(exc))
    st.code("python scripts/train_model.py --generate-sample --n-units 90", language="bash")
    st.stop()

with st.sidebar:
    st.header("筛选器 / Filters")
    selected_risks = st.multiselect(
        "故障风险 / Failure risk",
        options=["high", "medium", "low"],
        default=["high", "medium", "low"],
        format_func=bilingual_risk,
    )
    max_rul = st.slider("最大预测 RUL / Max predicted RUL", min_value=0, max_value=125, value=125, step=5)
    selected_unit = st.selectbox(
        "设备详情 / Asset detail",
        options=sorted(fleet_df["unit_id"].unique()),
        format_func=lambda value: f"设备 {value} / Asset {value}",
    )

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
kpi_columns[0].metric("资产数量 / Fleet assets", f"{len(fleet_df):,}")
kpi_columns[1].metric("高风险资产 / High-risk assets", f"{high_risk_count:,}")
kpi_columns[2].metric("RUL 中位数 / Median predicted RUL", format_metric(median_rul))
kpi_columns[3].metric("故障窗口召回率 / Failure horizon recall", f"{recall:.0%}")

left, right = st.columns([1.35, 1])

with left:
    st.subheader("维护干预队列 / Maintenance Intervention Queue")
    queue_columns = [
        "unit_id",
        "cycle",
        "predicted_rul",
        "prediction_interval_low",
        "prediction_interval_high",
        "failure_risk",
        "maintenance_action",
    ]
    queue_display = filtered[queue_columns].head(25).copy()
    queue_display["failure_risk"] = queue_display["failure_risk"].apply(bilingual_risk)
    queue_display["maintenance_action"] = queue_display["maintenance_action"].apply(bilingual_action)
    queue_display = queue_display.rename(
        columns={
            "unit_id": "设备 ID / Unit ID",
            "cycle": "当前周期 / Cycle",
            "predicted_rul": "预测 RUL / Predicted RUL",
            "prediction_interval_low": "区间下限 / Interval Low",
            "prediction_interval_high": "区间上限 / Interval High",
            "failure_risk": "故障风险 / Failure Risk",
            "maintenance_action": "维护建议 / Maintenance Action",
        }
    )
    st.dataframe(queue_display, use_container_width=True, hide_index=True)

with right:
    st.subheader("风险分布 / Risk Mix")
    risk_mix = fleet_df["failure_risk"].value_counts().reindex(["high", "medium", "low"]).fillna(0)
    risk_mix.index = [bilingual_risk(value) for value in risk_mix.index]
    st.bar_chart(risk_mix)

st.subheader("各设备预测 RUL / Predicted RUL by Asset")
chart_data = filtered[["unit_id", "predicted_rul"]].set_index("unit_id").head(40)
st.bar_chart(chart_data)

detail_left, detail_right = st.columns([1, 1])

with detail_left:
    st.subheader("选中设备 / Selected Asset")
    asset_row = fleet_df[fleet_df["unit_id"] == selected_unit].iloc[0]
    st.write(
        {
            "设备 ID / unit_id": int(asset_row["unit_id"]),
            "最新周期 / latest_cycle": int(asset_row["cycle"]),
            "预测 RUL / predicted_rul": float(asset_row["predicted_rul"]),
            "故障风险 / failure_risk": bilingual_risk(asset_row["failure_risk"]),
            "维护建议 / recommended_action": bilingual_action(asset_row["maintenance_action"]),
        }
    )

with detail_right:
    st.subheader("模型验证 / Model Validation")
    validation_metrics = pd.DataFrame(
        [
            {"指标 / metric": "MAE", "数值 / value": model_metrics["mae"]},
            {"指标 / metric": "RMSE", "数值 / value": model_metrics["rmse"]},
            {"指标 / metric": "Bias", "数值 / value": model_metrics["bias"]},
            {"指标 / metric": "20 周期内 / Within 20 cycles", "数值 / value": model_metrics["within_20_cycles_pct"]},
            {"指标 / metric": "故障窗口 Precision / Horizon precision", "数值 / value": model_metrics["failure_horizon_precision"]},
            {"指标 / metric": "故障窗口 Recall / Horizon recall", "数值 / value": model_metrics["failure_horizon_recall"]},
        ]
    )
    st.dataframe(validation_metrics, use_container_width=True, hide_index=True)

st.subheader("评估散点图 / Evaluation Scatter")
scatter = eval_df[["rul", "predicted_rul"]].rename(columns={"rul": "actual_rul"})
st.scatter_chart(scatter, x="actual_rul", y="predicted_rul")

st.caption(
    "仅用于决策支持演示。风险阈值和维护建议在生产使用前需要领域校准。 / "
    "Demo decision support only. Risk thresholds and maintenance actions require domain calibration before production use."
)
