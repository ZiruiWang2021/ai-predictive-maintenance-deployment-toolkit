"""Generate the offline CMAPSS-style sample data."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from pdm_toolkit.data import SampleDataConfig, save_sample_data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate synthetic run-to-failure sensor data.")
    parser.add_argument("--output", default="data/raw/sample_turbofan_sensor_log.csv")
    parser.add_argument("--n-units", type=int, default=90)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = PROJECT_ROOT / args.output
    config = SampleDataConfig(n_units=args.n_units, seed=args.seed)
    save_sample_data(output_path, config=config)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
