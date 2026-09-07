"""Invalid value rules and email validation."""

from __future__ import annotations

import re

import pandas as pd

from app.utils.constants import EMAIL_COLUMNS
from app.utils.helpers import is_numeric_series

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")

# Column-name keyed validation rules used by the cleaning pipeline.
COLUMN_RULES: dict[str, dict] = {
    "age": {"min": 0, "max": 120},
    "salary": {"min": 0},
    "quantity": {"min": 0},
    "unit_price": {"min": 0},
    "total_sales": {"min": 0},
}


def is_valid_email(value: object) -> bool:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return False
    text = str(value).strip()
    if not text:
        return False
    return bool(EMAIL_REGEX.match(text))


def detect_invalid_mask(df: pd.DataFrame) -> pd.DataFrame:
    """Return a boolean DataFrame where True marks invalid cells."""
    mask = pd.DataFrame(False, index=df.index, columns=df.columns)

    for column in df.columns:
        col_key = str(column).strip().lower()
        series = df[column]

        if col_key in EMAIL_COLUMNS:
            mask[column] = series.apply(
                lambda v: False if pd.isna(v) or str(v).strip() == "" else not is_valid_email(v)
            )
            continue

        rule = COLUMN_RULES.get(col_key)
        if rule and is_numeric_series(series):
            numeric = pd.to_numeric(series, errors="coerce")
            invalid = pd.Series(False, index=series.index)
            if "min" in rule:
                invalid |= numeric < rule["min"]
            if "max" in rule:
                invalid |= numeric > rule["max"]
            # NaN from coercion of non-numeric dirty values also count as invalid when original present
            coerced_invalid = series.notna() & numeric.isna() & ~series.astype(str).str.strip().eq("")
            mask[column] = invalid.fillna(False) | coerced_invalid
            continue

        if col_key in {"date", "order_date", "purchase_date"}:
            text = series.astype(str).str.strip()
            present = series.notna() & text.ne("") & text.ne("nan")
            parsed = pd.to_datetime(series, errors="coerce", format="mixed", dayfirst=True)
            # Fall back for mixed common formats when pandas cannot parse as mixed
            still_bad = present & parsed.isna()
            if still_bad.any():
                for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d"):
                    retry = pd.to_datetime(series[still_bad], errors="coerce", format=fmt)
                    parsed.loc[still_bad] = parsed.loc[still_bad].fillna(retry)
                    still_bad = present & parsed.isna()
                    if not still_bad.any():
                        break
            mask[column] = still_bad

    return mask


def count_invalid_values(df: pd.DataFrame) -> int:
    return int(detect_invalid_mask(df).sum().sum())


def summarize_invalid_values(df: pd.DataFrame) -> dict[str, int]:
    mask = detect_invalid_mask(df)
    return {col: int(mask[col].sum()) for col in mask.columns if int(mask[col].sum()) > 0}
