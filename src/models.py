"""Forecasting models and training helpers for the Bike Sharing project."""

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression


def naive_forecast(y: pd.Series | np.ndarray, lag: int = 1) -> np.ndarray:
    """Predict each observation from a previous observation without wraparound."""
    values = np.asarray(y, dtype=float).reshape(-1)
    if lag < 1:
        raise ValueError("lag must be at least 1.")

    predictions = np.full(values.shape, np.nan, dtype=float)
    predictions[lag:] = values[:-lag]
    return predictions


def moving_average_forecast(
    y: pd.Series | np.ndarray,
    window: int = 24,
) -> np.ndarray:
    """Predict each observation from the preceding rolling mean."""
    if window < 1:
        raise ValueError("window must be at least 1.")
    series = pd.Series(np.asarray(y, dtype=float).reshape(-1))
    return series.shift(1).rolling(window=window, min_periods=window).mean().to_numpy()


def build_linear_regression() -> LinearRegression:
    """Create a linear-regression baseline."""
    return LinearRegression()


def build_random_forest(
    random_state: int = 42,
    n_estimators: int = 300,
    max_depth: int | None = None,
) -> RandomForestRegressor:
    """Create a reproducible Random Forest regressor."""
    return RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state,
        n_jobs=-1,
    )


def make_windows_for_indices(
    features: np.ndarray,
    target: np.ndarray,
    target_indices: Iterable[int],
    lookback: int = 24,
    horizon: int = 1,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Create sequence windows whose targets fall at the requested row indices.

    For horizon=1, a target at row ``t`` uses feature rows ``t-lookback:t``.
    Returning the retained target indices makes it possible to align predictions
    with timestamps after windows near the start of the data are discarded.
    """
    x = np.asarray(features, dtype=np.float32)
    y = np.asarray(target, dtype=np.float32).reshape(-1)
    indices = np.asarray(list(target_indices), dtype=int)

    if x.ndim != 2:
        raise ValueError("features must have shape (rows, features).")
    if len(x) != len(y):
        raise ValueError("features and target must contain the same number of rows.")
    if lookback < 1 or horizon < 1:
        raise ValueError("lookback and horizon must be at least 1.")

    windows: list[np.ndarray] = []
    targets: list[float] = []
    retained_indices: list[int] = []

    for target_index in indices:
        input_end = target_index - horizon + 1
        input_start = input_end - lookback
        if input_start < 0 or input_end > len(x) or target_index >= len(y):
            continue
        windows.append(x[input_start:input_end])
        targets.append(float(y[target_index]))
        retained_indices.append(int(target_index))

    if not windows:
        raise ValueError("No valid windows could be created for the requested indices.")

    return (
        np.stack(windows).astype(np.float32),
        np.asarray(targets, dtype=np.float32),
        np.asarray(retained_indices, dtype=int),
    )
