"""Data quality scoring and before/after reports."""

from __future__ import annotations

import pandas as pd

from app.schemas.quality import QualityResponse, QualityScoreBreakdown, QualitySnapshot
from app.services.validator import count_invalid_values
from app.utils.helpers import clamp, interpret_quality_score, safe_percentage


def _snapshot(df: pd.DataFrame, outliers: int = 0) -> QualitySnapshot:
    return QualitySnapshot(
        rows=int(len(df)),
        missing_values=int(df.isna().sum().sum()),
        duplicates=int(df.duplicated().sum()),
        invalid_values=count_invalid_values(df),
        outliers=outliers,
    )


def _component_from_rate(bad_rate_percent: float) -> float:
    """Map a bad-rate percentage to a 0–100 score (100 = perfect)."""
    return clamp(100.0 - bad_rate_percent)


def calculate_quality_scores(df: pd.DataFrame) -> tuple[float, QualityScoreBreakdown]:
    rows = max(int(len(df)), 1)
    cells = max(rows * max(int(df.shape[1]), 1), 1)

    missing_rate = safe_percentage(int(df.isna().sum().sum()), cells)
    duplicate_rate = safe_percentage(int(df.duplicated().sum()), rows)
    invalid_count = count_invalid_values(df)
    invalid_rate = safe_percentage(invalid_count, cells)

    # Consistency: inconsistent casing categories + malformed emails approximated via invalid rate weight
    object_cols = [c for c in df.columns if df[c].dtype == object or str(df[c].dtype) == "string"]
    inconsistent = 0
    for col in object_cols:
        series = df[col].dropna().astype(str).str.strip()
        if series.empty:
            continue
        lower_unique = series.str.lower().nunique()
        raw_unique = series.nunique()
        if raw_unique > lower_unique:
            inconsistent += raw_unique - lower_unique
    consistency_rate = safe_percentage(inconsistent + invalid_count, max(cells, 1))

    breakdown = QualityScoreBreakdown(
        missing_score=_component_from_rate(missing_rate),
        duplicate_score=_component_from_rate(duplicate_rate),
        invalid_score=_component_from_rate(invalid_rate),
        consistency_score=_component_from_rate(consistency_rate),
    )
    final = clamp(
        0.30 * breakdown.missing_score
        + 0.25 * breakdown.duplicate_score
        + 0.25 * breakdown.invalid_score
        + 0.20 * breakdown.consistency_score
    )
    return round(final, 2), breakdown


def build_quality_report(
    dataset_id: int,
    before_df: pd.DataFrame,
    after_df: pd.DataFrame,
    outliers_after: int = 0,
) -> QualityResponse:
    before = _snapshot(before_df)
    after = _snapshot(after_df, outliers=outliers_after)
    score, breakdown = calculate_quality_scores(after_df)
    return QualityResponse(
        dataset_id=dataset_id,
        before=before,
        after=after,
        quality_score=score,
        interpretation=interpret_quality_score(score),
        breakdown=breakdown,
    )
