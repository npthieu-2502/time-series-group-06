"""
Script tạo file data/processed/bike_sharing_processed.csv
từ data/raw/hour.csv sử dụng pipeline trong src/features.py

Chạy từ thư mục gốc của project:
    python scripts/generate_processed_data.py
"""

import os
import sys

# Thêm thư mục gốc vào path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import pandas as pd
from src.features import (
    add_datetime_column,
    add_time_features,
    add_fourier_features,
    add_lag_features,
    remove_outliers_iqr,
    split_data,
)

RAW_PATH = os.path.join(ROOT, "data", "raw", "hour.csv")
PROCESSED_PATH = os.path.join(ROOT, "data", "processed", "bike_sharing_processed.csv")

print(f"Loading: {RAW_PATH}")
df = pd.read_csv(RAW_PATH)
print(f"Shape raw: {df.shape}")

# Pipeline
df = remove_outliers_iqr(df, target="cnt", lower_q=0.01, upper_q=0.99)
df = add_datetime_column(df)
df = add_time_features(df)
df = add_fourier_features(df)
df = add_lag_features(df, target="cnt")

# Drop leakage columns
DROP_COLS = ["casual", "registered", "dteday", "instant"]
existing_drop = [c for c in DROP_COLS if c in df.columns]
df = df.drop(columns=existing_drop)

# Drop NaN from lag features
n_before = len(df)
df = df.dropna().reset_index(drop=True)
print(f"Dropped {n_before - len(df)} NaN rows (from lag features)")

# Split
df_train, df_val, df_test = split_data(df)
df_train = df_train.copy(); df_train["split"] = "train"
df_val = df_val.copy(); df_val["split"] = "val"
df_test = df_test.copy(); df_test["split"] = "test"

df_final = pd.concat([df_train, df_val, df_test], ignore_index=True)
df_final = df_final.sort_values("datetime").reset_index(drop=True)

os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)
df_final.to_csv(PROCESSED_PATH, index=False)
print(f"\n✓ Saved to: {PROCESSED_PATH}")
print(f"  Shape: {df_final.shape}")
print(f"  Columns: {list(df_final.columns)}")
