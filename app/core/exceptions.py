"""Application-specific exceptions and error codes."""

from typing import Any


class AppError(Exception):
    """Base application error with a stable machine-readable code."""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class InvalidFileTypeError(AppError):
    def __init__(self, message: str = "Unsupported file type.") -> None:
        super().__init__("INVALID_FILE_TYPE", message, status_code=400)


class FileTooLargeError(AppError):
    def __init__(self, message: str = "Uploaded file exceeds the size limit.") -> None:
        super().__init__("FILE_TOO_LARGE", message, status_code=413)


class EmptyFileError(AppError):
    def __init__(self, message: str = "Uploaded file is empty.") -> None:
        super().__init__("EMPTY_FILE", message, status_code=400)


class InvalidDatasetError(AppError):
    def __init__(self, message: str = "Dataset is invalid or cannot be parsed.") -> None:
        super().__init__("INVALID_DATASET", message, status_code=400)


class DatasetNotFoundError(AppError):
    def __init__(self, dataset_id: int) -> None:
        super().__init__(
            "DATASET_NOT_FOUND",
            f"Dataset with id {dataset_id} was not found.",
            status_code=404,
        )


class DatasetNotCleanedError(AppError):
    def __init__(self, dataset_id: int) -> None:
        super().__init__(
            "DATASET_NOT_CLEANED",
            f"Dataset with id {dataset_id} has not been cleaned yet.",
            status_code=400,
        )


class ProcessingError(AppError):
    def __init__(self, message: str = "An error occurred while processing the dataset.") -> None:
        super().__init__("PROCESSING_ERROR", message, status_code=500)


class InvalidCleaningConfigurationError(AppError):
    def __init__(self, message: str = "Cleaning configuration is invalid.") -> None:
        super().__init__("INVALID_CLEANING_CONFIGURATION", message, status_code=422)


class UnsupportedOperationError(AppError):
    def __init__(self, message: str = "Requested operation is not supported.") -> None:
        super().__init__("UNSUPPORTED_OPERATION", message, status_code=400)
