"""Pydantic schemas for dataset endpoints."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DatasetUploadResponse(BaseModel):
    dataset_id: int
    filename: str
    file_type: str
    rows: int
    columns: int
    status: str


class DatasetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    file_type: str
    original_path: str
    cleaned_path: str | None = None
    rows: int
    columns: int
    status: str
    created_at: datetime
    updated_at: datetime


class DatasetListResponse(BaseModel):
    items: list[DatasetResponse]
    page: int
    page_size: int
    total: int
    total_pages: int


class MessageResponse(BaseModel):
    message: str = Field(..., examples=["Dataset deleted successfully."])
