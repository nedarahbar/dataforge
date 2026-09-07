"""Cleaning configuration and response schemas."""

from typing import Literal

from pydantic import BaseModel, Field


class CleaningConfig(BaseModel):
    remove_duplicates: bool = True
    fill_missing: bool = True
    normalize_text: bool = True
    validate_values: bool = True
    detect_outliers: bool = True
    numeric_strategy: Literal["median", "mean", "zero"] = "median"
    categorical_strategy: Literal["mode", "empty", "unknown"] = "mode"


class CleaningResultResponse(BaseModel):
    dataset_id: int
    status: str
    rows_before: int
    rows_after: int
    duplicates_removed: int
    missing_values_filled: int
    invalid_values_detected: int
    outliers_detected: int
    cleaning_id: int | None = None


class CleaningHistoryItem(BaseModel):
    id: int
    dataset_id: int
    configuration: dict
    rows_before: int
    rows_after: int
    duplicates_removed: int
    missing_values_filled: int
    invalid_values_detected: int
    outliers_detected: int
    status: str
    created_at: str
