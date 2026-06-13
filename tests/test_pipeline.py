"""Pipeline smoke tests using only standard-library unittest."""

from __future__ import annotations

from pathlib import Path
import shutil
import sys
import tempfile
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import pandas as pd

from pdm_toolkit.data import SampleDataConfig, add_rul_labels, generate_cmapss_style_sample
from pdm_toolkit.features import build_feature_table, feature_columns
from pdm_toolkit.pipeline import build_demo_artifacts


class PipelineTests(unittest.TestCase):
    def test_sample_generation_and_labels(self) -> None:
        frame = generate_cmapss_style_sample(SampleDataConfig(n_units=8, min_life=20, max_life=25, seed=7))
        labelled = add_rul_labels(frame, failure_horizon=5)
        self.assertEqual(labelled["unit_id"].nunique(), 8)
        self.assertIn("rul", labelled.columns)
        self.assertEqual(int(labelled.groupby("unit_id")["rul"].min().max()), 0)

    def test_feature_table_has_numeric_features(self) -> None:
        frame = generate_cmapss_style_sample(SampleDataConfig(n_units=6, min_life=20, max_life=25, seed=11))
        features = build_feature_table(add_rul_labels(frame))
        cols = feature_columns(features)
        self.assertGreater(len(cols), 20)
        self.assertFalse(features[cols].isna().any().any())

    def test_end_to_end_demo_artifacts(self) -> None:
        temp_dir = Path(tempfile.mkdtemp(prefix="pdm_toolkit_test_"))
        try:
            result = build_demo_artifacts(temp_dir, n_units=18, seed=9, train_share=0.7)
            self.assertTrue(result["fleet_path"].exists())
            self.assertTrue(result["model_path"].exists())
            fleet = pd.read_csv(result["fleet_path"])
            self.assertIn("predicted_rul", fleet.columns)
            self.assertGreater(len(fleet), 0)
            self.assertGreater(result["metrics"]["rmse"], 0)
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
