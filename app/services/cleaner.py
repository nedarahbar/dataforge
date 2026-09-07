"""Configurable data cleaning pipeline."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from app.schemas.cleaning import CleaningConfig
from app.services.validator import count_invalid_values
from app.utils.constants import EMAIL_COLUMNS, PROTECTED_TEXT_COLUMNS
from app.utils.helpers import is_numeric_series


@dataclass
class CleaningResult:
    dataframe: pd.DataFrame
    rows_before: int
    rows_after: int
    duplicates_removed: int
    missing_values_filled: int
    invalid_values_detected: int
    outliers_detected: int
    empty_columns: list[str]
    outlier_details: dict[str, int]


def _fill_missing(df: pd.DataFrame, config: CleaningConfig) -> tuple[pd.DataFrame, int]:
    filled = 0
    result = df.copy()
    for column in result.columns:
        series = result[column]
        missing_mask = series.isna()
        missing_count = int(missing_mask.sum())
        if missing_count == 0:
            continue
        if missing_count == len(result):
            # Completely empty column: report only, do not delete / fill blindly
            continue

        if is_numeric_series(series):
            numeric = pd.to_numeric(series, errors="coerce")
            if config.numeric_strategy == "median":
                fill_value = numeric.median()
            elif config.numeric_strategy == "mean":
                fill_value = numeric.mean()
            else:
                fill_value = 0
            if pd.isna(fill_value):
                continue
            result.loc[missing_mask, column] = fill_value
            filled += missing_count
        else:
            col_key = str(column).strip().lower()
            if config.categorical_strategy == "mode":
                if col_key in EMAIL_COLUMNS:
                    from app.services.validator import is_valid_email

                    valid = series.dropna()[series.dropna().map(is_valid_email)]
                    mode = valid.mode()
                    fill_value = mode.iloc[0] if not mode.empty else "unknown@example.com"
                else:
                    mode = series.mode(dropna=True)
                    fill_value = mode.iloc[0] if not mode.empty else "Unknown"
            elif config.categorical_strategy == "empty":
                fill_value = ""
            else:
                fill_value = "Unknown"
            result.loc[missing_mask, column] = fill_value
            filled += missing_count
    return result, filled


def _normalize_text(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    for column in result.columns:
        col_key = str(column).strip().lower()
        if col_key in PROTECTED_TEXT_COLUMNS or col_key in EMAIL_COLUMNS:
            continue
        if is_numeric_series(result[column]):
            continue

        series = result[column].astype("string")
        cleaned = series.str.strip().str.replace(r"\s+", " ", regex=True)

        # Build canonical mapping from lowercase form -> most common original Title Case form
        non_null = cleaned.dropna()
        if non_null.empty:
            result[column] = cleaned
            continue

        lower_map: dict[str, str] = {}
        for value in non_null:
            key = value.lower()
            if key not in lower_map:
                # Prefer Title Case for multi-word categories
                lower_map[key] = value.title() if value.lower() == value or value.isupper() else value.strip().title()
            # If existing mapping is already title-like keep first stable choice

        result[column] = cleaned.map(lambda v: lower_map.get(v.lower(), v) if pd.notna(v) else v)
    return result


def _detect_outliers_iqr(df: pd.DataFrame) -> tuple[int, dict[str, int]]:
    total = 0
    details: dict[str, int] = {}
    for column in df.columns:
        series = df[column]
        if not is_numeric_series(series):
            continue
        numeric = pd.to_numeric(series, errors="coerce").dropna()
        if len(numeric) < 4:
            continue
        q1 = numeric.quantile(0.25)
        q3 = numeric.quantile(0.75)
        iqr = q3 - q1
        if iqr == 0:
            continue
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outliers = ((numeric < lower) | (numeric > upper)).sum()
        if outliers:
            details[str(column)] = int(outliers)
            total += int(outliers)
    return total, details


def clean_dataframe(df: pd.DataFrame, config: CleaningConfig) -> CleaningResult:
    """
    Run the configurable cleaning pipeline.

    Order: schema detect → missing → duplicates → text normalize →
    invalid detection → outlier detection → final validation.
    Outliers are reported, not removed, in v1.
    """
    working = df.copy()
    rows_before = int(len(working))
    empty_columns = [str(c) for c in working.columns if working[c].isna().all()]

    missing_values_filled = 0
    if config.fill_missing:
        working, missing_values_filled = _fill_missing(working, config)

    duplicates_removed = 0
    if config.remove_duplicates:
        before_dup = int(len(working))
        working = working.drop_duplicates().reset_index(drop=True)
        duplicates_removed = before_dup - int(len(working))

    if config.normalize_text:
        working = _normalize_text(working)

    invalid_values_detected = 0
    if config.validate_values:
        # Detect and report only — do not silently rewrite values in v1
        invalid_values_detected = count_invalid_values(working)

    outliers_detected = 0
    outlier_details: dict[str, int] = {}
    if config.detect_outliers:
        outliers_detected, outlier_details = _detect_outliers_iqr(working)

    rows_after = int(len(working))
    return CleaningResult(
        dataframe=working,
        rows_before=rows_before,
        rows_after=rows_after,
        duplicates_removed=duplicates_removed,
        missing_values_filled=missing_values_filled,
        invalid_values_detected=invalid_values_detected,
        outliers_detected=outliers_detected,
        empty_columns=empty_columns,
        outlier_details=outlier_details,
    )
