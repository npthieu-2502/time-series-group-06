"""Feature engineering utilities for time-series forecasting."""

import numpy as np
import pandas as pd


def add_datetime_column(df: pd.DataFrame) -> pd.DataFrame:
    """Create a full hourly datetime column from dteday and hr."""
    result = df.copy()
    result["datetime"] = pd.to_datetime(result["dteday"]) + pd.to_timedelta(result["hr"], unit="h")
    return result.sort_values("datetime").reset_index(drop=True)


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add basic calendar features."""
    result = df.copy()
    result["hour"] = result["datetime"].dt.hour
    result["day_of_week"] = result["datetime"].dt.dayofweek
    result["month"] = result["datetime"].dt.month
    result["is_weekend"] = result["day_of_week"].isin([5, 6]).astype(int)
    return result


def add_fourier_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add cyclic Fourier features for hour, weekday, and month."""
    result = df.copy()
    result["hour_sin"] = np.sin(2 * np.pi * result["hour"] / 24)
    result["hour_cos"] = np.cos(2 * np.pi * result["hour"] / 24)
    result["weekday_sin"] = np.sin(2 * np.pi * result["day_of_week"] / 7)
    result["weekday_cos"] = np.cos(2 * np.pi * result["day_of_week"] / 7)
    result["month_sin"] = np.sin(2 * np.pi * result["month"] / 12)
    result["month_cos"] = np.cos(2 * np.pi * result["month"] / 12)
    return result


def add_lag_features(df: pd.DataFrame, target: str = "cnt") -> pd.DataFrame:
    """Add lag and rolling features for the target variable."""
    result = df.copy()
    result["lag_1"] = result[target].shift(1)
    result["lag_24"] = result[target].shift(24)
    result["lag_168"] = result[target].shift(168)
    result["rolling_mean_24"] = result[target].shift(1).rolling(window=24).mean()
    result["rolling_std_24"] = result[target].shift(1).rolling(window=24).std()
    return result
