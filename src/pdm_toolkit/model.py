"""Small transparent RUL model implemented with numpy."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import pickle

import numpy as np
import pandas as pd


@dataclass
class RidgeRULModel:
    feature_columns: list[str]
    coefficients: np.ndarray
    intercept: float
    means: np.ndarray
    stds: np.ndarray
    residual_q10: float
    residual_q90: float
    target_cap: float = 125.0

    def predict(self, features: pd.DataFrame | np.ndarray) -> np.ndarray:
        """Predict clipped RUL values."""
        matrix = features.to_numpy(dtype=float) if isinstance(features, pd.DataFrame) else np.asarray(features, dtype=float)
        matrix = (matrix - self.means) / self.stds
        predictions = matrix @ self.coefficients + self.intercept
        return np.clip(predictions, 0, self.target_cap)

    def prediction_interval(self, predictions: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Create a simple empirical residual interval."""
        low = np.clip(predictions + self.residual_q10, 0, self.target_cap)
        high = np.clip(predictions + self.residual_q90, 0, self.target_cap)
        return low, high


def train_ridge_rul_model(
    train_frame: pd.DataFrame,
    feature_cols: list[str],
    alpha: float = 15.0,
    target_cap: float = 125.0,
) -> RidgeRULModel:
    """Train a ridge regression model on capped RUL labels."""
    x = train_frame[feature_cols].to_numpy(dtype=float)
    y = train_frame["rul"].clip(upper=target_cap).to_numpy(dtype=float)

    means = x.mean(axis=0)
    stds = x.std(axis=0)
    stds[stds == 0] = 1.0
    x_scaled = (x - means) / stds
    x_design = np.column_stack([np.ones(len(x_scaled)), x_scaled])

    penalty = np.eye(x_design.shape[1]) * alpha
    penalty[0, 0] = 0.0
    weights = np.linalg.pinv(x_design.T @ x_design + penalty) @ x_design.T @ y

    fitted = x_design @ weights
    residuals = y - fitted
    return RidgeRULModel(
        feature_columns=feature_cols,
        coefficients=weights[1:],
        intercept=float(weights[0]),
        means=means,
        stds=stds,
        residual_q10=float(np.quantile(residuals, 0.10)),
        residual_q90=float(np.quantile(residuals, 0.90)),
        target_cap=target_cap,
    )


def evaluate_predictions(actual: np.ndarray, predicted: np.ndarray, horizon: int = 30) -> dict[str, float]:
    """Compute regression and threshold metrics."""
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    error = predicted - actual
    actual_failure = actual <= horizon
    predicted_failure = predicted <= horizon
    true_positive = np.logical_and(actual_failure, predicted_failure).sum()
    false_positive = np.logical_and(~actual_failure, predicted_failure).sum()
    false_negative = np.logical_and(actual_failure, ~predicted_failure).sum()

    precision = true_positive / max(true_positive + false_positive, 1)
    recall = true_positive / max(true_positive + false_negative, 1)
    return {
        "mae": float(np.mean(np.abs(error))),
        "rmse": float(np.sqrt(np.mean(error**2))),
        "bias": float(np.mean(error)),
        "within_20_cycles_pct": float((np.abs(error) <= 20).mean()),
        "failure_horizon_precision": float(precision),
        "failure_horizon_recall": float(recall),
    }


def save_model(model: RidgeRULModel, output_path: str | Path) -> Path:
    """Persist the model as a pickle artifact."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as handle:
        pickle.dump(model, handle)
    return output_path


def load_model(path: str | Path) -> RidgeRULModel:
    """Load a model artifact."""
    with Path(path).open("rb") as handle:
        model = pickle.load(handle)
    if not isinstance(model, RidgeRULModel):
        raise TypeError("Loaded artifact is not a RidgeRULModel")
    return model
