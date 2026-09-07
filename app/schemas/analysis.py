"""Analysis response schemas."""

from pydantic import BaseModel


class NumericStats(BaseModel):
    count: int
    mean: float | None = None
    median: float | None = None
    min: float | None = None
    max: float | None = None
    std: float | None = None
    p25: float | None = None
    p50: float | None = None
    p75: float | None = None


class CategoryFrequency(BaseModel):
    value: str
    count: int
    percentage: float


class CategoricalStats(BaseModel):
    unique_count: int
    top_categories: list[CategoryFrequency]


class BusinessAnalysis(BaseModel):
    total_sales: float | None = None
    average_sales: float | None = None
    top_products: list[CategoryFrequency] | None = None
    top_customers: list[CategoryFrequency] | None = None
    sales_by_region: list[CategoryFrequency] | None = None
    monthly_sales: list[dict] | None = None


class AnalysisResponse(BaseModel):
    dataset_id: int
    rows: int
    columns: int
    numeric: dict[str, NumericStats]
    categorical: dict[str, CategoricalStats]
    business: BusinessAnalysis | None = None
