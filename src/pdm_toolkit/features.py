"""Feature engineering for run-to-failure sensor histories."""

from __future__ import annotations

import numpy as np
import pandas as pd

from pdm_toolkit.config import SENSOR_COLUMNS


def build_feature_table(frame: pd.DataFrame) -> pd.DataFrame:
    """Create modelling features from asset-cycle sensor rows."""
    data = frame.sort_values(["unit_id", "cycle"]).copy()
    data["cycle_log"] = np.log1p(data["cycle"])

    for column in SENSOR_COLUMNS:
        grouped = data.groupby("unit_id", group_keys=False)[column]
        data[f"{column}_delta"] = grouped.diff().fillna(0.0)
        data[f"{column}_roll5_mean"] = grouped.rolling(5, min_periods=1).mean().reset_index(level=0, drop=True)
        data[f"{column}_roll5_std"] = (
            grouped.rolling(5, min_periods=2).std().reset_index(level=0, drop=True).fillna(0.0)
        )
        data[f"{column}_roll15_mean"] = grouped.rolling(15, min_periods=1).mean().reset_index(level=0, drop=True)
        data[f"{column}_trend"] = data[f"{column}_roll5_mean"] - data[f"{column}_roll15_mean"]

    data["thermal_margin_proxy"] = data["sensor_01"] - data["sensor_03"]
    data["vibration_proxy"] = data["sensor_09"] * data["sensor_12"]
    data["efficiency_proxy"] = data["sensor_06"] / data["sensor_02"].replace(0, np.nan)
    data["efficiency_proxy"] = data["efficiency_proxy"].fillna(data["efficiency_proxy"].median())

    if "asset_class" in data.columns:
        asset_class_dummies = pd.get_dummies(data["asset_class"], prefix="asset_class", dtype=float)
        data = pd.concat([data, asset_class_dummies], axis=1)

    return data.replace([np.inf, -np.inf], np.nan).fillna(0.0)


def feature_columns(frame: pd.DataFrame) -> list[str]:
    """Return model feature columns from a feature table."""
    excluded = {
        "unit_id",
        "cycle",
        "rul",
        "failure_within_horizon",
        "maintenance_action",
        "failure_risk",
        "predicted_rul",
        "prediction_interval_low",
        "prediction_interval_high",
    }
    candidates = [column for column in frame.columns if column not in excluded]
    return [column for column in candidates if pd.api.types.is_numeric_dtype(frame[column])]


def align_features(frame: pd.DataFrame, expected_columns: list[str]) -> pd.DataFrame:
    """Align a feature table to the model's expected columns."""
    aligned = frame.copy()
    for column in expected_columns:
        if column not in aligned.columns:
            aligned[column] = 0.0
    return aligned[expected_columns]
