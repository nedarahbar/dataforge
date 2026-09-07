"""Dataset HTTP routes."""

from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.logging import get_logger
from app.database.database import get_db
from app.schemas.analysis import AnalysisResponse
from app.schemas.cleaning import CleaningConfig, CleaningResultResponse
from app.schemas.dataset import DatasetListResponse, DatasetResponse, DatasetUploadResponse
from app.schemas.profile import ProfileResponse
from app.schemas.quality import QualityResponse
from app.services import dataset_service, file_handler

router = APIRouter(prefix="/datasets", tags=["Datasets"])
logger = get_logger(__name__)


@router.post(
    "/upload",
    response_model=DatasetUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a CSV or Excel dataset",
)
async def upload_dataset(
    file: UploadFile = File(..., description="CSV or Excel file"),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> DatasetUploadResponse:
    content = await file_handler.read_upload_bytes(file, settings)
    extension = file_handler.validate_upload(file, content, settings)
    return dataset_service.upload_dataset(
        db,
        filename=file.filename or "upload.csv",
        extension=extension,
        content=content,
    )


@router.get(
    "",
    response_model=DatasetListResponse,
    summary="List uploaded datasets with pagination",
)
def list_datasets(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> DatasetListResponse:
    return dataset_service.list_datasets(db, page=page, page_size=page_size)


@router.get(
    "/{dataset_id}",
    response_model=DatasetResponse,
    summary="Get dataset details",
)
def get_dataset(dataset_id: int, db: Session = Depends(get_db)) -> DatasetResponse:
    return dataset_service.get_dataset(db, dataset_id)


@router.get(
    "/{dataset_id}/profile",
    response_model=ProfileResponse,
    summary="Profile a dataset before cleaning",
)
def profile_dataset(dataset_id: int, db: Session = Depends(get_db)) -> ProfileResponse:
    return dataset_service.profile_dataset(db, dataset_id)


@router.post(
    "/{dataset_id}/clean",
    response_model=CleaningResultResponse,
    summary="Run configurable cleaning pipeline",
)
def clean_dataset(
    dataset_id: int,
    config: CleaningConfig | None = None,
    db: Session = Depends(get_db),
) -> CleaningResultResponse:
    return dataset_service.clean_dataset(db, dataset_id, config or CleaningConfig())


@router.get(
    "/{dataset_id}/quality",
    response_model=QualityResponse,
    summary="Before/after quality report and score",
)
def quality_report(dataset_id: int, db: Session = Depends(get_db)) -> QualityResponse:
    return dataset_service.quality_report(db, dataset_id)


@router.get(
    "/{dataset_id}/analysis",
    response_model=AnalysisResponse,
    summary="Analyze the cleaned dataset",
)
def analyze_dataset(dataset_id: int, db: Session = Depends(get_db)) -> AnalysisResponse:
    return dataset_service.analyze_dataset(db, dataset_id)


@router.get(
    "/{dataset_id}/download",
    summary="Download the cleaned dataset as CSV",
    responses={200: {"content": {"text/csv": {}}}},
)
def download_dataset(dataset_id: int, db: Session = Depends(get_db)) -> FileResponse:
    path, download_name = dataset_service.get_download_path(db, dataset_id)
    return FileResponse(
        path=path,
        media_type="text/csv",
        filename=download_name,
    )


@router.delete(
    "/{dataset_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete dataset, files, and cleaning history",
)
def delete_dataset(dataset_id: int, db: Session = Depends(get_db)) -> None:
    dataset_service.delete_dataset(db, dataset_id)


@router.get(
    "/{dataset_id}/cleaning-history",
    summary="List cleaning operations for a dataset",
)
def cleaning_history(dataset_id: int, db: Session = Depends(get_db)) -> list[dict]:
    return dataset_service.get_cleaning_history(db, dataset_id)
