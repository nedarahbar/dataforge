"""Quality report schemas."""

from pydantic import BaseModel, Field


class QualitySnapshot(BaseModel):
    rows: int
    missing_values: int
    duplicates: int
    invalid_values: int
    outliers: int = 0


class QualityScoreBreakdown(BaseModel):
    missing_score: float
    duplicate_score: float
    invalid_score: float
    consistency_score: float


class QualityResponse(BaseModel):
    dataset_id: int
    before: QualitySnapshot
    after: QualitySnapshot
    quality_score: float = Field(..., ge=0, le=100)
    interpretation: str
    breakdown: QualityScoreBreakdown | None = None
