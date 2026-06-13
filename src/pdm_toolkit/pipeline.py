"""End-to-end training and scoring pipeline."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

import pandas as pd

from pdm_toolkit.config import DEFAULT_FAILURE_HORIZON
from pdm_toolkit.data import SampleDataConfig, add_rul_labels, load_sensor_log, save_sample_data
from pdm_toolkit.features import align_features, build_feature_table, feature_columns
from pdm_toolkit.model import evaluate_predictions, save_model, train_ridge_rul_model
from pdm_toolkit.scoring import add_operational_recommendations


def split_units(frame: pd.DataFrame, train_share: float = 0.75) -> tuple[set[int], set[int]]:
    """Create deterministic unit-level train and evaluation splits."""
    units = sorted(frame["unit_id"].unique())
    split_at = max(1, int(len(units) * train_share))
    return set(units[:split_at]), set(units[split_at:])


def current_fleet_snapshot(frame: pd.DataFrame) -> pd.DataFrame:
    """Select a deterministic pseudo-live observation for each asset."""
    selected_rows = []
    for unit_id, group in frame.sort_values(["unit_id", "cycle"]).groupby("unit_id"):
        max_cycle = int(group["cycle"].max())
        fraction = 0.35 + (((int(unit_id) * 37) % 60) / 100)
        target_cycle = max(1, min(max_cycle, int(max_cycle * fraction)))
        row_index = group[group["cycle"] <= target_cycle]["cycle"].idxmax()
        selected_rows.append(frame.loc[row_index])
    return pd.DataFrame(selected_rows).sort_values("unit_id").reset_index(drop=True)


def train_and_score(
    project_root: str | Path,
    raw_path: str | Path,
    train_share: float = 0.75,
    failure_horizon: int = DEFAULT_FAILURE_HORIZON,
) -> dict[str, Path | dict[str, float]]:
    """Train the model and write dashboard-ready artifacts."""
    root = Path(project_root)
    processed_dir = root / "data" / "processed"
    artifact_dir = root / "artifacts"
    processed_dir.mkdir(parents=True, exist_ok=True)
    artifact_dir.mkdir(parents=True, exist_ok=True)

    raw = load_sensor_log(raw_path)
    labelled = add_rul_labels(raw, failure_horizon=failure_horizon)
    features = build_feature_table(labelled)
    train_units, eval_units = split_units(features, train_share=train_share)
    train_frame = features[features["unit_id"].isin(train_units)].copy()
    eval_frame = features[features["unit_id"].isin(eval_units)].copy()
    cols = feature_columns(features)

    model = train_ridge_rul_model(train_frame, cols)
    eval_x = align_features(eval_frame, model.feature_columns)
    eval_predictions = model.predict(eval_x)
    low, high = model.prediction_interval(eval_predictions)
    eval_output = eval_frame[["unit_id", "cycle", "rul", "failure_within_horizon"]].copy()
    eval_output["predicted_rul"] = eval_predictions.round(2)
    eval_output["prediction_interval_low"] = low.round(2)
    eval_output["prediction_interval_high"] = high.round(2)
    eval_output = add_operational_recommendations(eval_output)

    latest = current_fleet_snapshot(features)
    latest_x = align_features(latest, model.feature_columns)
    latest_predictions = model.predict(latest_x)
    latest_low, latest_high = model.prediction_interval(latest_predictions)
    fleet_output_columns = ["unit_id", "cycle", "rul", "failure_within_horizon"]
    for optional in ["asset_class", "failure_mode"]:
        if optional in latest.columns:
            fleet_output_columns.append(optional)
    fleet_output = latest[fleet_output_columns].copy()
    fleet_output["predicted_rul"] = latest_predictions.round(2)
    fleet_output["prediction_interval_low"] = latest_low.round(2)
    fleet_output["prediction_interval_high"] = latest_high.round(2)
    fleet_output = add_operational_recommendations(fleet_output)

    metrics = evaluate_predictions(
        eval_frame["rul"].clip(upper=model.target_cap).to_numpy(),
        eval_predictions,
        horizon=failure_horizon,
    )
    metrics.update(
        {
            "train_units": float(len(train_units)),
            "evaluation_units": float(len(eval_units)),
            "feature_count": float(len(model.feature_columns)),
            "failure_horizon_cycles": float(failure_horizon),
        }
    )

    feature_path = processed_dir / "model_features.csv"
    eval_path = processed_dir / "evaluation_predictions.csv"
    fleet_path = processed_dir / "fleet_latest_predictions.csv"
    model_path = artifact_dir / "rul_ridge_model.pkl"
    metrics_path = artifact_dir / "model_metrics.json"

    features.to_csv(feature_path, index=False)
    eval_output.to_csv(eval_path, index=False)
    fleet_output.to_csv(fleet_path, index=False)
    save_model(model, model_path)
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    return {
        "feature_path": feature_path,
        "evaluation_path": eval_path,
        "fleet_path": fleet_path,
        "model_path": model_path,
        "metrics_path": metrics_path,
        "metrics": metrics,
    }


def build_demo_artifacts(
    project_root: str | Path,
    n_units: int = 90,
    seed: int = 42,
    train_share: float = 0.75,
) -> dict[str, Path | dict[str, float]]:
    """Generate the sample dataset, train the model, and score the fleet."""
    root = Path(project_root)
    raw_path = root / "data" / "raw" / "sample_turbofan_sensor_log.csv"
    config = SampleDataConfig(n_units=n_units, seed=seed)
    save_sample_data(raw_path, config=config)
    result = train_and_score(root, raw_path=raw_path, train_share=train_share)
    metadata_path = root / "artifacts" / "demo_data_metadata.json"
    metadata_path.write_text(json.dumps(asdict(config), indent=2), encoding="utf-8")
    result["raw_path"] = raw_path
    result["metadata_path"] = metadata_path
    return result
