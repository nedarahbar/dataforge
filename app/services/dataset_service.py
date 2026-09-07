"""Dataset orchestration: upload, CRUD, clean, quality, analysis, download."""

from __future__ import annotations

import json
import math
from pathlib import Path

from sqlalchemy.orm import Session

from app.core.exceptions import DatasetNotCleanedError, DatasetNotFoundError, ProcessingError
from app.core.logging import get_logger
from app.database.models import CleaningOperation, Dataset
from app.schemas.cleaning import CleaningConfig, CleaningResultResponse
from app.schemas.dataset import DatasetListResponse, DatasetResponse, DatasetUploadResponse
from app.services import analyzer, cleaner, file_handler, profiler, quality
from app.utils.constants import CleaningStatus, DatasetStatus

logger = get_logger(__name__)


def _get_dataset_or_404(db: Session, dataset_id: int) -> Dataset:
    dataset = db.get(Dataset, dataset_id)
    if dataset is None or dataset.status == DatasetStatus.DELETED.value:
        raise DatasetNotFoundError(dataset_id)
    return dataset


def upload_dataset(
    db: Session,
    *,
    filename: str,
    extension: str,
    content: bytes,
) -> DatasetUploadResponse:
    logger.info("File upload started: filename=%s size=%s", filename, len(content))
    df = file_handler.parse_dataframe(content, extension)

    dataset = Dataset(
        filename=file_handler.safe_storage_name(filename),
        file_type=extension,
        original_path="",  # filled after id is known
        cleaned_path=None,
        rows=int(len(df)),
        columns=int(df.shape[1]),
        status=DatasetStatus.UPLOADED.value,
    )
    db.add(dataset)
    db.flush()

    path = file_handler.save_raw_file(dataset.id, content, extension)
    dataset.original_path = str(path)
    db.commit()
    db.refresh(dataset)

    logger.info("File upload completed: dataset_id=%s rows=%s cols=%s", dataset.id, dataset.rows, dataset.columns)
    return DatasetUploadResponse(
        dataset_id=dataset.id,
        filename=dataset.filename,
        file_type=dataset.file_type,
        rows=dataset.rows,
        columns=dataset.columns,
        status=dataset.status,
    )


def list_datasets(db: Session, page: int = 1, page_size: int = 20) -> DatasetListResponse:
    page = max(page, 1)
    page_size = min(max(page_size, 1), 100)
    query = db.query(Dataset).filter(Dataset.status != DatasetStatus.DELETED.value)
    total = query.count()
    items = (
        query.order_by(Dataset.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return DatasetListResponse(
        items=[DatasetResponse.model_validate(item) for item in items],
        page=page,
        page_size=page_size,
        total=total,
        total_pages=max(1, math.ceil(total / page_size)) if total else 0,
    )


def get_dataset(db: Session, dataset_id: int) -> DatasetResponse:
    return DatasetResponse.model_validate(_get_dataset_or_404(db, dataset_id))


def profile_dataset(db: Session, dataset_id: int):
    dataset = _get_dataset_or_404(db, dataset_id)
    df = file_handler.load_dataframe_from_path(dataset.original_path)
    result = profiler.profile_dataframe(df, dataset.id)
    if dataset.status == DatasetStatus.UPLOADED.value:
        dataset.status = DatasetStatus.PROFILED.value
        db.commit()
    return result


def clean_dataset(db: Session, dataset_id: int, config: CleaningConfig) -> CleaningResultResponse:
    dataset = _get_dataset_or_404(db, dataset_id)
    logger.info("Cleaning started: dataset_id=%s", dataset_id)
    dataset.status = DatasetStatus.CLEANING.value
    db.commit()

    try:
        df = file_handler.load_dataframe_from_path(dataset.original_path)
        result = cleaner.clean_dataframe(df, config)
        cleaned_path = file_handler.save_cleaned_dataframe(dataset.id, result.dataframe)

        operation = CleaningOperation(
            dataset_id=dataset.id,
            configuration=config.model_dump_json(),
            rows_before=result.rows_before,
            rows_after=result.rows_after,
            duplicates_removed=result.duplicates_removed,
            missing_values_filled=result.missing_values_filled,
            invalid_values_detected=result.invalid_values_detected,
            outliers_detected=result.outliers_detected,
            status=CleaningStatus.COMPLETED.value,
        )
        db.add(operation)

        dataset.cleaned_path = str(cleaned_path)
        dataset.rows = result.rows_after
        dataset.status = DatasetStatus.CLEANED.value
        db.commit()
        db.refresh(operation)

        logger.info(
            "Cleaning completed: dataset_id=%s rows_before=%s rows_after=%s",
            dataset_id,
            result.rows_before,
            result.rows_after,
        )
        return CleaningResultResponse(
            dataset_id=dataset.id,
            status=dataset.status,
            rows_before=result.rows_before,
            rows_after=result.rows_after,
            duplicates_removed=result.duplicates_removed,
            missing_values_filled=result.missing_values_filled,
            invalid_values_detected=result.invalid_values_detected,
            outliers_detected=result.outliers_detected,
            cleaning_id=operation.id,
        )
    except Exception as exc:  # noqa: BLE001
        dataset.status = DatasetStatus.FAILED.value
        db.commit()
        logger.exception("Processing error during cleaning: dataset_id=%s", dataset_id)
        if isinstance(exc, ProcessingError):
            raise
        raise ProcessingError(str(exc)) from exc


def quality_report(db: Session, dataset_id: int):
    dataset = _get_dataset_or_404(db, dataset_id)
    if dataset.status != DatasetStatus.CLEANED.value or not dataset.cleaned_path:
        raise DatasetNotCleanedError(dataset_id)

    before_df = file_handler.load_dataframe_from_path(dataset.original_path)
    after_df = file_handler.load_dataframe_from_path(dataset.cleaned_path)

    latest = (
        db.query(CleaningOperation)
        .filter(CleaningOperation.dataset_id == dataset.id)
        .order_by(CleaningOperation.id.desc())
        .first()
    )
    outliers = latest.outliers_detected if latest else 0
    return quality.build_quality_report(dataset.id, before_df, after_df, outliers_after=outliers)


def analyze_dataset(db: Session, dataset_id: int):
    dataset = _get_dataset_or_404(db, dataset_id)
    if dataset.status != DatasetStatus.CLEANED.value or not dataset.cleaned_path:
        raise DatasetNotCleanedError(dataset_id)
    df = file_handler.load_dataframe_from_path(dataset.cleaned_path)
    return analyzer.analyze_dataframe(df, dataset.id)


def get_download_path(db: Session, dataset_id: int) -> tuple[Path, str]:
    dataset = _get_dataset_or_404(db, dataset_id)
    if dataset.status != DatasetStatus.CLEANED.value or not dataset.cleaned_path:
        raise DatasetNotCleanedError(dataset_id)
    path = Path(dataset.cleaned_path)
    if not path.exists():
        raise ProcessingError("Cleaned dataset file is missing from storage.")
    download_name = f"{Path(dataset.filename).stem}_cleaned.csv"
    return path, download_name


def delete_dataset(db: Session, dataset_id: int) -> None:
    dataset = _get_dataset_or_404(db, dataset_id)
    logger.info("Dataset deletion started: dataset_id=%s", dataset_id)

    for path_str in [dataset.original_path, dataset.cleaned_path]:
        if path_str:
            path = Path(path_str)
            if path.exists():
                path.unlink()

    db.delete(dataset)
    db.commit()
    logger.info("Dataset deletion completed: dataset_id=%s", dataset_id)


def get_cleaning_history(db: Session, dataset_id: int) -> list[dict]:
    dataset = _get_dataset_or_404(db, dataset_id)
    ops = (
        db.query(CleaningOperation)
        .filter(CleaningOperation.dataset_id == dataset.id)
        .order_by(CleaningOperation.id.desc())
        .all()
    )
    history = []
    for op in ops:
        try:
            configuration = json.loads(op.configuration)
        except json.JSONDecodeError:
            configuration = {"raw": op.configuration}
        history.append(
            {
                "id": op.id,
                "dataset_id": op.dataset_id,
                "configuration": configuration,
                "rows_before": op.rows_before,
                "rows_after": op.rows_after,
                "duplicates_removed": op.duplicates_removed,
                "missing_values_filled": op.missing_values_filled,
                "invalid_values_detected": op.invalid_values_detected,
                "outliers_detected": op.outliers_detected,
                "status": op.status,
                "created_at": op.created_at.isoformat() if op.created_at else None,
            }
        )
    return history
