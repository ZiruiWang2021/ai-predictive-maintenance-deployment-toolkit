"""Data generation, loading, and cleaning utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from pdm_toolkit.config import IDENTIFIER_COLUMNS, SENSOR_COLUMNS, SETTING_COLUMNS


@dataclass(frozen=True)
class SampleDataConfig:
    n_units: int = 90
    min_life: int = 115
    max_life: int = 230
    seed: int = 42


def generate_cmapss_style_sample(config: SampleDataConfig | None = None) -> pd.DataFrame:
    """Generate a deterministic, CMAPSS-style run-to-failure sensor dataset."""
    config = config or SampleDataConfig()
    rng = np.random.default_rng(config.seed)
    records: list[dict[str, float | int | str]] = []
    sensor_base = np.array([640, 1585, 1400, 14.5, 21.6, 554, 2388, 9050, 1.3, 47.0, 520, 39.0])
    sensor_drift = np.array([18, 33, 28, -2.2, 2.9, -35, 5, -85, 0.8, 4.7, -42, 2.6])
    condition_weights = np.array([10, -8, 6, 0.6, -0.4, 14, 2, -20, 0.1, 0.8, 10, -0.5])
    failure_modes = ["compressor_wear", "fan_efficiency_loss", "bearing_degradation"]

    for unit_id in range(1, config.n_units + 1):
        asset_class = rng.choice(["route-critical", "standard", "low-criticality"], p=[0.25, 0.55, 0.20])
        failure_mode = rng.choice(failure_modes, p=[0.45, 0.30, 0.25])
        design_life = int(rng.integers(config.min_life, config.max_life + 1))
        operating_offset = rng.normal(0, 0.2)
        mode_multiplier = {
            "compressor_wear": 1.10,
            "fan_efficiency_loss": 0.85,
            "bearing_degradation": 1.25,
        }[failure_mode]

        for cycle in range(1, design_life + 1):
            cycle_ratio = cycle / design_life
            degradation = cycle_ratio**2.1 * mode_multiplier
            setting_1 = rng.normal(0.0 + operating_offset, 0.35)
            setting_2 = rng.normal(0.0, 0.25)
            setting_3 = rng.choice([0.0, 1.0, 2.0], p=[0.65, 0.25, 0.10])
            operating_condition = 0.5 * setting_1 - 0.3 * setting_2 + 0.15 * setting_3
            noise = rng.normal(0, [3.0, 5.0, 4.0, 0.4, 0.3, 6.0, 0.8, 15.0, 0.06, 0.5, 6.0, 0.4])
            sensors = sensor_base + sensor_drift * degradation + condition_weights * operating_condition + noise

            row: dict[str, float | int | str] = {
                "unit_id": unit_id,
                "cycle": cycle,
                "asset_class": asset_class,
                "failure_mode": failure_mode,
                "setting_1": round(float(setting_1), 5),
                "setting_2": round(float(setting_2), 5),
                "setting_3": round(float(setting_3), 5),
            }
            row.update({col: round(float(value), 5) for col, value in zip(SENSOR_COLUMNS, sensors)})
            records.append(row)

    return pd.DataFrame.from_records(records)


def save_sample_data(output_path: str | Path, config: SampleDataConfig | None = None) -> Path:
    """Generate and save the sample dataset."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data = generate_cmapss_style_sample(config)
    data.to_csv(output_path, index=False)
    return output_path


def load_sensor_log(path: str | Path) -> pd.DataFrame:
    """Load a sensor log CSV and apply baseline cleaning."""
    frame = pd.read_csv(path)
    return clean_sensor_log(frame)


def clean_sensor_log(frame: pd.DataFrame) -> pd.DataFrame:
    """Clean the sensor log without leaking future failure labels."""
    required = set(IDENTIFIER_COLUMNS + SETTING_COLUMNS + SENSOR_COLUMNS)
    missing = required.difference(frame.columns)
    if missing:
        missing_text = ", ".join(sorted(missing))
        raise ValueError(f"Sensor log is missing required columns: {missing_text}")

    cleaned = frame.copy()
    for column in IDENTIFIER_COLUMNS + SETTING_COLUMNS + SENSOR_COLUMNS:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    cleaned = cleaned.dropna(subset=IDENTIFIER_COLUMNS)
    cleaned = cleaned.sort_values(["unit_id", "cycle"]).drop_duplicates(["unit_id", "cycle"], keep="last")

    numeric_columns = SETTING_COLUMNS + SENSOR_COLUMNS
    cleaned[numeric_columns] = cleaned.groupby("unit_id", group_keys=False)[numeric_columns].apply(
        lambda group: group.interpolate(limit_direction="both")
    )
    cleaned[numeric_columns] = cleaned[numeric_columns].fillna(cleaned[numeric_columns].median(numeric_only=True))
    cleaned["unit_id"] = cleaned["unit_id"].astype(int)
    cleaned["cycle"] = cleaned["cycle"].astype(int)

    if "asset_class" not in cleaned.columns:
        cleaned["asset_class"] = "unknown"
    if "failure_mode" not in cleaned.columns:
        cleaned["failure_mode"] = "unknown"

    return cleaned.reset_index(drop=True)


def add_rul_labels(frame: pd.DataFrame, failure_horizon: int = 30) -> pd.DataFrame:
    """Add RUL and binary horizon labels to a complete run-to-failure dataset."""
    labelled = frame.copy()
    max_cycles = labelled.groupby("unit_id")["cycle"].transform("max")
    labelled["rul"] = (max_cycles - labelled["cycle"]).clip(lower=0)
    labelled["failure_within_horizon"] = (labelled["rul"] <= failure_horizon).astype(int)
    return labelled
