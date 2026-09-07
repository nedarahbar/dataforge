"""Dataset profiling service."""

from __future__ import annotations

import pandas as pd

from app.schemas.profile import ColumnProfile, ProfileResponse
from app.services.validator import count_invalid_values
from app.utils.helpers import is_numeric_series, safe_percentage


def profile_dataframe(df: pd.DataFrame, dataset_id: int) -> ProfileResponse:
    rows = int(len(df))
    columns = int(df.shape[1])
    duplicate_rows = int(df.duplicated().sum())
    total_missing = int(df.isna().sum().sum())
    total_invalid = count_invalid_values(df)

    columns_profile: list[ColumnProfile] = []
    for name in df.columns:
        series = df[name]
        missing_count = int(series.isna().sum())
        unique_count = int(series.nunique(dropna=True))
        profile = ColumnProfile(
            name=str(name),
            dtype=str(series.dtype),
            missing_count=missing_count,
            missing_percentage=safe_percentage(missing_count, rows),
            unique_count=unique_count,
            unique_percentage=safe_percentage(unique_count, rows),
        )

        if is_numeric_series(series):
            numeric = pd.to_numeric(series, errors="coerce")
            if numeric.notna().any():
                profile.min = float(numeric.min())
                profile.max = float(numeric.max())
                profile.mean = float(round(numeric.mean(), 4))
                profile.median = float(round(numeric.median(), 4))
                profile.std = float(round(numeric.std(ddof=1), 4)) if numeric.notna().sum() > 1 else 0.0

        columns_profile.append(profile)

    return ProfileResponse(
        dataset_id=dataset_id,
        rows=rows,
        columns=columns,
        duplicate_rows=duplicate_rows,
        total_missing_values=total_missing,
        total_invalid_values=total_invalid,
        columns_profile=columns_profile,
    )
