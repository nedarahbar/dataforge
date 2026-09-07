"""Profiling response schemas."""

from pydantic import BaseModel


class ColumnProfile(BaseModel):
    name: str
    dtype: str
    missing_count: int
    missing_percentage: float
    unique_count: int
    unique_percentage: float | None = None
    min: float | None = None
    max: float | None = None
    mean: float | None = None
    median: float | None = None
    std: float | None = None


class ProfileResponse(BaseModel):
    dataset_id: int
    rows: int
    columns: int
    duplicate_rows: int
    total_missing_values: int
    total_invalid_values: int
    columns_profile: list[ColumnProfile]
