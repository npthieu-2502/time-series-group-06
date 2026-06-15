"""Model utilities for the bike sharing forecasting project."""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression


def naive_forecast(y: pd.Series | np.ndarray) -> np.ndarray:
    """Predict the next value by using the previous observed value."""
    values = np.asarray(y)
    return np.roll(values, 1)


def moving_average_forecast(y: pd.Series | np.ndarray, window: int = 24) -> np.ndarray:
    """Predict using a rolling moving average."""
    series = pd.Series(y)
    return series.shift(1).rolling(window=window).mean().to_numpy()


def build_linear_regression() -> LinearRegression:
    """Create a linear regression baseline."""
    return LinearRegression()


def build_random_forest(random_state: int = 42) -> RandomForestRegressor:
    """Create a random forest regressor."""
    return RandomForestRegressor(
        n_estimators=200,
        random_state=random_state,
        n_jobs=-1,
    )
