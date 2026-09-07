"""Generic helper utilities."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from app.utils.constants import QUALITY_INTERPRETATION


def sanitize_filename(filename: str) -> str:
    """Return a basename-only, traversal-safe filename."""
    name = Path(filename).name
    name = re.sub(r"[^\w.\- ]+", "_", name).strip()
    return name or "upload.bin"


def clamp(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
    return max(lower, min(upper, value))


def interpret_quality_score(score: float) -> str:
    rounded = clamp(score)
    for (low, high), label in QUALITY_INTERPRETATION.items():
        if low <= rounded <= high:
            return label
    return "Critical"


def is_numeric_series(series: pd.Series) -> bool:
    return pd.api.types.is_numeric_dtype(series)


def is_datetime_like(series: pd.Series) -> bool:
    if pd.api.types.is_datetime64_any_dtype(series):
        return True
    sample = series.dropna().astype(str).head(20)
    if sample.empty:
        return False
    parsed = pd.to_datetime(sample, errors="coerce", dayfirst=False)
    return parsed.notna().mean() >= 0.7


def safe_percentage(part: float, whole: float) -> float:
    if whole <= 0:
        return 0.0
    return round((part / whole) * 100, 2)
