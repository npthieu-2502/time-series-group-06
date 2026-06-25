"""Feature engineering utilities for time-series forecasting.

Pipeline tổng quát:
    df_raw  ->  add_datetime_column
            ->  add_time_features
            ->  add_fourier_features
            ->  add_lag_features
            ->  remove_outliers
            ->  normalize_features
            ->  split_data
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


# ---------------------------------------------------------------------------
# 1. Datetime
# ---------------------------------------------------------------------------

def add_datetime_column(df: pd.DataFrame) -> pd.DataFrame:
    """Create a full hourly datetime column from dteday and hr."""
    result = df.copy()
    result["datetime"] = pd.to_datetime(result["dteday"]) + pd.to_timedelta(result["hr"], unit="h")
    return result.sort_values("datetime").reset_index(drop=True)


# ---------------------------------------------------------------------------
# 2. Calendar / Time features
# ---------------------------------------------------------------------------

def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add basic calendar features."""
    result = df.copy()
    result["hour"] = result["datetime"].dt.hour
    result["day_of_week"] = result["datetime"].dt.dayofweek
    result["month"] = result["datetime"].dt.month
    result["is_weekend"] = result["day_of_week"].isin([5, 6]).astype(int)
    return result


# ---------------------------------------------------------------------------
# 3. Fourier / Cyclic features
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# 4. Lag & Rolling features
# ---------------------------------------------------------------------------

def add_lag_features(df: pd.DataFrame, target: str = "cnt") -> pd.DataFrame:
    """Add lag and rolling features for the target variable.

    Lag features:
        lag_1   : giá trị 1 giờ trước.
        lag_24  : giá trị cùng giờ hôm qua.
        lag_168 : giá trị cùng giờ tuần trước.
    Rolling features (tính trên shift(1) để tránh data leakage):
        rolling_mean_24 : trung bình 24 giờ gần nhất.
        rolling_std_24  : độ lệch chuẩn 24 giờ gần nhất.
    """
    result = df.copy()
    result["lag_1"] = result[target].shift(1)
    result["lag_24"] = result[target].shift(24)
    result["lag_168"] = result[target].shift(168)
    result["rolling_mean_24"] = result[target].shift(1).rolling(window=24).mean()
    result["rolling_std_24"] = result[target].shift(1).rolling(window=24).std()
    return result


# ---------------------------------------------------------------------------
# 5. Outlier handling
# ---------------------------------------------------------------------------

def remove_outliers_iqr(
    df: pd.DataFrame,
    target: str = "cnt",
    lower_q: float = 0.01,
    upper_q: float = 0.99,
) -> pd.DataFrame:
    """Cap outliers in the target column using quantile clipping (Winsorization).

    Thay vì xóa hàng, ta clip giá trị về ngưỡng [Q1%, Q99%] để giữ
    tính liên tục của chuỗi thời gian.
    """
    result = df.copy()
    low = result[target].quantile(lower_q)
    high = result[target].quantile(upper_q)
    n_clipped = ((result[target] < low) | (result[target] > high)).sum()
    result[target] = result[target].clip(low, high)
    print(f"[remove_outliers_iqr] Clipped {n_clipped} rows in '{target}' "
          f"to [{low:.1f}, {high:.1f}]")
    return result


# ---------------------------------------------------------------------------
# 6. Normalization
# ---------------------------------------------------------------------------

def normalize_features(
    df_train: pd.DataFrame,
    df_val: pd.DataFrame,
    df_test: pd.DataFrame,
    feature_cols: list,
) -> tuple:
    """Fit StandardScaler on train, transform all splits.

    Returns:
        df_train_scaled, df_val_scaled, df_test_scaled, scaler
    """
    scaler = StandardScaler()
    df_train_s = df_train.copy()
    df_val_s = df_val.copy()
    df_test_s = df_test.copy()

    df_train_s[feature_cols] = scaler.fit_transform(df_train[feature_cols])
    df_val_s[feature_cols] = scaler.transform(df_val[feature_cols])
    df_test_s[feature_cols] = scaler.transform(df_test[feature_cols])

    return df_train_s, df_val_s, df_test_s, scaler


# ---------------------------------------------------------------------------
# 7. Train / Val / Test split
# ---------------------------------------------------------------------------

def split_data(
    df: pd.DataFrame,
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
) -> tuple:
    """Split data chronologically into train / validation / test.

    Tỷ lệ mặc định: 70 / 15 / 15 (không xáo trộn để giữ thứ tự thời gian).

    Returns:
        df_train, df_val, df_test
    """
    n = len(df)
    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))

    df_train = df.iloc[:train_end].copy()
    df_val = df.iloc[train_end:val_end].copy()
    df_test = df.iloc[val_end:].copy()

    print(f"[split_data] Total: {n} rows")
    print(f"  Train : {len(df_train):>6} rows  ({len(df_train)/n*100:.1f}%)")
    print(f"  Val   : {len(df_val):>6} rows  ({len(df_val)/n*100:.1f}%)")
    print(f"  Test  : {len(df_test):>6} rows  ({len(df_test)/n*100:.1f}%)")
    return df_train, df_val, df_test


# ---------------------------------------------------------------------------
# 8. Full pipeline
# ---------------------------------------------------------------------------

def build_feature_pipeline(
    raw_df: pd.DataFrame,
    target: str = "cnt",
    drop_cols: list | None = None,
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    normalize: bool = True,
) -> dict:
    """Run the full feature engineering pipeline end-to-end.

    Steps:
        1. Add datetime column.
        2. Add time / calendar features.
        3. Add Fourier cyclic features.
        4. Add lag & rolling features.
        5. Drop rows with NaN (caused by lag/rolling windows).
        6. Drop columns not needed (casual, registered, dteday, …).
        7. Split chronologically 70/15/15.
        8. Optionally normalize numeric feature columns (fit on train only).

    Returns:
        dict with keys:
            df_train, df_val, df_test         — final DataFrames (after norm)
            df_train_raw, df_val_raw, df_test_raw — before normalization
            scaler                             — fitted StandardScaler (or None)
            feature_cols                       — list of feature column names
    """
    if drop_cols is None:
        drop_cols = ["casual", "registered", "dteday", "instant"]

    df = raw_df.copy()

    # Steps 1–4
    df = add_datetime_column(df)
    df = add_time_features(df)
    df = add_fourier_features(df)
    df = add_lag_features(df, target=target)

    # Drop unwanted columns
    existing_drop = [c for c in drop_cols if c in df.columns]
    df = df.drop(columns=existing_drop)

    # Drop NaN rows from lag/rolling
    n_before = len(df)
    df = df.dropna().reset_index(drop=True)
    print(f"[pipeline] Dropped {n_before - len(df)} NaN rows after lag features.")

    # Split
    df_train_raw, df_val_raw, df_test_raw = split_data(df, train_ratio, val_ratio)

    # Feature columns = everything except target and datetime
    non_feature = {target, "datetime"}
    feature_cols = [c for c in df.columns if c not in non_feature]

    # Normalize
    scaler = None
    if normalize:
        df_train, df_val, df_test, scaler = normalize_features(
            df_train_raw, df_val_raw, df_test_raw, feature_cols
        )
    else:
        df_train, df_val, df_test = df_train_raw.copy(), df_val_raw.copy(), df_test_raw.copy()

    return {
        "df_train": df_train,
        "df_val": df_val,
        "df_test": df_test,
        "df_train_raw": df_train_raw,
        "df_val_raw": df_val_raw,
        "df_test_raw": df_test_raw,
        "scaler": scaler,
        "feature_cols": feature_cols,
    }
