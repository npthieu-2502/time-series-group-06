"""Evaluation metrics and plots for forecasting models."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def _aligned_finite_values(y_true, y_pred) -> tuple[np.ndarray, np.ndarray]:
    actual = np.asarray(y_true, dtype=float).reshape(-1)
    predicted = np.asarray(y_pred, dtype=float).reshape(-1)
    if len(actual) != len(predicted):
        raise ValueError("y_true and y_pred must have the same length.")

    valid = np.isfinite(actual) & np.isfinite(predicted)
    if not valid.any():
        raise ValueError("No finite prediction pairs are available for evaluation.")
    return actual[valid], predicted[valid]


def mae(y_true, y_pred) -> float:
    """Mean Absolute Error."""
    actual, predicted = _aligned_finite_values(y_true, y_pred)
    return float(np.mean(np.abs(actual - predicted)))


def rmse(y_true, y_pred) -> float:
    """Root Mean Squared Error."""
    actual, predicted = _aligned_finite_values(y_true, y_pred)
    return float(np.sqrt(np.mean((actual - predicted) ** 2)))


def mape(y_true, y_pred, epsilon: float = 1e-8) -> float:
    """MAPE computed only where the actual value is non-zero."""
    actual, predicted = _aligned_finite_values(y_true, y_pred)
    non_zero = np.abs(actual) > epsilon
    if not non_zero.any():
        return float("nan")
    return float(
        np.mean(np.abs((actual[non_zero] - predicted[non_zero]) / actual[non_zero]))
        * 100
    )


def smape(y_true, y_pred, epsilon: float = 1e-8) -> float:
    """Symmetric Mean Absolute Percentage Error."""
    actual, predicted = _aligned_finite_values(y_true, y_pred)
    denominator = (np.abs(actual) + np.abs(predicted)) / 2
    valid = denominator > epsilon
    if not valid.any():
        return 0.0
    return float(
        np.mean(np.abs(actual[valid] - predicted[valid]) / denominator[valid]) * 100
    )


def evaluate_predictions(y_true, y_pred) -> dict[str, float]:
    """Calculate all metrics required by the assignment."""
    return {
        "mae": mae(y_true, y_pred),
        "rmse": rmse(y_true, y_pred),
        "mape": mape(y_true, y_pred),
        "smape": smape(y_true, y_pred),
    }


def build_metrics_table(
    y_true,
    predictions: Mapping[str, np.ndarray | pd.Series],
) -> pd.DataFrame:
    """Build one comparison row per model."""
    rows = []
    for model_name, model_predictions in predictions.items():
        row = {"model": model_name}
        row.update(evaluate_predictions(y_true, model_predictions))
        rows.append(row)
    return pd.DataFrame(rows).sort_values("rmse").reset_index(drop=True)


def plot_predictions(
    timestamps,
    y_true,
    predictions: Mapping[str, np.ndarray | pd.Series],
    output_path: str | Path,
    max_points: int = 336,
) -> None:
    """Plot actual and predicted values for a readable test-set segment."""
    actual = np.asarray(y_true, dtype=float).reshape(-1)
    time_values = np.asarray(timestamps)
    if len(actual) != len(time_values):
        raise ValueError("timestamps and y_true must have the same length.")

    count = min(max_points, len(actual))
    figure, axis = plt.subplots(figsize=(16, 6))
    axis.plot(time_values[:count], actual[:count], label="Giá trị thực tế", linewidth=2)

    for model_name, model_predictions in predictions.items():
        predicted = np.asarray(model_predictions, dtype=float).reshape(-1)
        if len(predicted) != len(actual):
            raise ValueError(f"Predictions for {model_name} have an invalid length.")
        axis.plot(time_values[:count], predicted[:count], label=model_name, alpha=0.85)

    axis.set_title("So sánh giá trị thực tế và dự báo trên tập test")
    axis.set_xlabel("Thời gian")
    axis.set_ylabel("Số lượng xe thuê")
    axis.legend()
    axis.grid(alpha=0.25)
    figure.autofmt_xdate()
    figure.tight_layout()

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(destination, dpi=150, bbox_inches="tight")
    plt.close(figure)
