"""Shared project configuration."""

from __future__ import annotations

from pathlib import Path


SENSOR_COLUMNS = [f"sensor_{idx:02d}" for idx in range(1, 13)]
SETTING_COLUMNS = ["setting_1", "setting_2", "setting_3"]
IDENTIFIER_COLUMNS = ["unit_id", "cycle"]
LABEL_COLUMNS = ["rul", "failure_within_horizon"]

DEFAULT_FAILURE_HORIZON = 30
DEFAULT_RISK_THRESHOLDS = {
    "high": 30,
    "medium": 60,
}


def project_root_from_file(file_path: str | Path) -> Path:
    """Return the repository root from a file under this project."""
    path = Path(file_path).resolve()
    for parent in [path, *path.parents]:
        if (parent / "README.md").exists() and (parent / "src").exists():
            return parent
    return Path.cwd()
