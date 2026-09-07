"""File upload, validation, load, and storage helpers."""

from __future__ import annotations

import io
from pathlib import Path

import pandas as pd
from fastapi import UploadFile

from app.core.config import Settings, get_settings
from app.core.exceptions import (
    EmptyFileError,
    FileTooLargeError,
    InvalidDatasetError,
    InvalidFileTypeError,
    ProcessingError,
)
from app.core.logging import get_logger
from app.utils.constants import MIME_BY_EXTENSION
from app.utils.helpers import sanitize_filename

logger = get_logger(__name__)


def get_extension(filename: str) -> str:
    return Path(filename).suffix.lower().lstrip(".")


def validate_upload(file: UploadFile, content: bytes, settings: Settings | None = None) -> str:
    """Validate extension, size, emptiness, and MIME where possible."""
    settings = settings or get_settings()

    if not file.filename:
        raise InvalidFileTypeError("Filename is required.")

    extension = get_extension(file.filename)
    if extension not in settings.allowed_extension_set:
        raise InvalidFileTypeError(
            f"File type '{extension or 'unknown'}' is not allowed. "
            f"Allowed: {', '.join(sorted(settings.allowed_extension_set))}."
        )

    if not content:
        raise EmptyFileError()

    if len(content) > settings.max_file_size:
        raise FileTooLargeError(
            f"File size {len(content)} bytes exceeds limit of {settings.max_file_size} bytes."
        )

    content_type = (file.content_type or "").lower()
    allowed_mimes = MIME_BY_EXTENSION.get(extension, set())
    if content_type and allowed_mimes and content_type not in allowed_mimes:
        # Soft MIME check: reject only clearly wrong types
        if content_type.startswith("image/") or content_type.startswith("audio/"):
            raise InvalidFileTypeError(f"MIME type '{content_type}' does not match file extension.")

    return extension


def parse_dataframe(content: bytes, extension: str) -> pd.DataFrame:
    """Parse CSV/Excel bytes into a DataFrame with a header row."""
    try:
        buffer = io.BytesIO(content)
        if extension == "csv":
            df = pd.read_csv(buffer)
        elif extension in {"xlsx", "xls"}:
            df = pd.read_excel(buffer, engine="openpyxl" if extension == "xlsx" else None)
        else:
            raise InvalidFileTypeError(f"Unsupported extension: {extension}")
    except InvalidFileTypeError:
        raise
    except Exception as exc:  # noqa: BLE001 - wrap parse failures
        raise InvalidDatasetError(f"Failed to parse dataset: {exc}") from exc

    if df is None or df.empty:
        raise InvalidDatasetError("Dataset has no rows.")

    if df.columns is None or len(df.columns) == 0:
        raise InvalidDatasetError("Dataset must include a header row.")

    # Detect unnamed/missing header quality issues without rejecting
    unnamed = [c for c in df.columns if str(c).startswith("Unnamed")]
    if len(unnamed) == len(df.columns):
        raise InvalidDatasetError("Dataset appears to be missing a proper header row.")

    return df


def save_raw_file(dataset_id: int, content: bytes, extension: str, settings: Settings | None = None) -> Path:
    settings = settings or get_settings()
    settings.ensure_storage_dirs()
    path = settings.raw_storage_path / f"{dataset_id}_original.{extension}"
    path.write_bytes(content)
    return path


def save_cleaned_dataframe(
    dataset_id: int,
    df: pd.DataFrame,
    settings: Settings | None = None,
) -> Path:
    settings = settings or get_settings()
    settings.ensure_storage_dirs()
    path = settings.cleaned_storage_path / f"{dataset_id}_cleaned.csv"
    df.to_csv(path, index=False)
    return path


def load_dataframe_from_path(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise ProcessingError(f"Dataset file not found at {path}.")
    try:
        if path.suffix.lower() == ".csv":
            return pd.read_csv(path)
        if path.suffix.lower() in {".xlsx", ".xls"}:
            return pd.read_excel(path)
        raise InvalidDatasetError(f"Unsupported stored file type: {path.suffix}")
    except (InvalidDatasetError, ProcessingError):
        raise
    except Exception as exc:  # noqa: BLE001
        raise ProcessingError(f"Failed to load dataset file: {exc}") from exc


async def read_upload_bytes(file: UploadFile, settings: Settings | None = None) -> bytes:
    settings = settings or get_settings()
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = await file.read(1024 * 1024)
        if not chunk:
            break
        total += len(chunk)
        if total > settings.max_file_size:
            raise FileTooLargeError(
                f"File size exceeds limit of {settings.max_file_size} bytes."
            )
        chunks.append(chunk)
    return b"".join(chunks)


def safe_storage_name(original_filename: str) -> str:
    return sanitize_filename(original_filename)
