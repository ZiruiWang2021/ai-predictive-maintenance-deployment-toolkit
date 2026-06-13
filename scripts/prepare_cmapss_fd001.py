"""Prepare NASA C-MAPSS FD001 training data for this toolkit."""

from __future__ import annotations

import argparse
from pathlib import Path
import tempfile
import zipfile

import pandas as pd


CMAPSS_COLUMNS = ["unit_id", "cycle", "setting_1", "setting_2", "setting_3"] + [
    f"sensor_{idx:02d}" for idx in range(1, 22)
]


def locate_train_file(input_path: Path) -> Path:
    if input_path.is_dir():
        candidates = list(input_path.rglob("train_FD001.txt"))
        if candidates:
            return candidates[0]
    if input_path.suffix.lower() == ".zip":
        temp_dir = Path(tempfile.mkdtemp(prefix="cmapss_fd001_"))
        with zipfile.ZipFile(input_path) as archive:
            archive.extractall(temp_dir)
        candidates = list(temp_dir.rglob("train_FD001.txt"))
        if candidates:
            return candidates[0]
    raise FileNotFoundError("Could not find train_FD001.txt in the supplied path.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert C-MAPSS FD001 into the toolkit CSV schema.")
    parser.add_argument("--input", required=True, help="Path to CMAPSS ZIP or extracted folder.")
    parser.add_argument("--output", default="data/raw/cmapss_fd001_train.csv")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_root = Path(__file__).resolve().parents[1]
    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = project_root / input_path
    train_file = locate_train_file(input_path)
    frame = pd.read_csv(train_file, sep=r"\s+", header=None, names=CMAPSS_COLUMNS)
    keep_columns = ["unit_id", "cycle", "setting_1", "setting_2", "setting_3"] + [
        f"sensor_{idx:02d}" for idx in range(1, 13)
    ]
    output = frame[keep_columns].copy()
    output["asset_class"] = "cmapss_fd001"
    output["failure_mode"] = "turbofan_degradation"
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = project_root / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(output_path, index=False)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
