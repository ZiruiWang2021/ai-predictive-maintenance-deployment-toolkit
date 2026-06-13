"""Train the RUL model and create dashboard-ready outputs."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from pdm_toolkit.pipeline import build_demo_artifacts, train_and_score


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train and score the predictive maintenance demo model.")
    parser.add_argument("--raw-path", default=None, help="CSV sensor log path. If omitted, use or create sample data.")
    parser.add_argument("--generate-sample", action="store_true", help="Regenerate sample data before training.")
    parser.add_argument("--n-units", type=int, default=90, help="Number of synthetic assets when generating sample data.")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--train-share", type=float, default=0.75)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.generate_sample or args.raw_path is None:
        result = build_demo_artifacts(PROJECT_ROOT, n_units=args.n_units, seed=args.seed, train_share=args.train_share)
    else:
        result = train_and_score(PROJECT_ROOT, raw_path=PROJECT_ROOT / args.raw_path, train_share=args.train_share)

    metrics = result["metrics"]
    print("Training complete")
    print(f"MAE: {metrics['mae']:.2f}")
    print(f"RMSE: {metrics['rmse']:.2f}")
    print(f"Failure horizon recall: {metrics['failure_horizon_recall']:.2f}")
    print(f"Fleet scores: {result['fleet_path']}")


if __name__ == "__main__":
    main()
