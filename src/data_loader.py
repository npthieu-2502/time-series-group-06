"""Data loading utilities for the bike sharing forecasting project."""

from pathlib import Path

import pandas as pd


def load_hourly_bike_data(path: str | Path) -> pd.DataFrame:
    """Load the raw hourly bike sharing dataset."""
    data_path = Path(path)
    return pd.read_csv(data_path)
