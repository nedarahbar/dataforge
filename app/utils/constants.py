"""Shared constants."""

from enum import StrEnum


class DatasetStatus(StrEnum):
    UPLOADED = "UPLOADED"
    PROFILED = "PROFILED"
    CLEANING = "CLEANING"
    CLEANED = "CLEANED"
    FAILED = "FAILED"
    DELETED = "DELETED"


class CleaningStatus(StrEnum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


QUALITY_INTERPRETATION = {
    (90, 100): "Excellent",
    (75, 89): "Good",
    (60, 74): "Fair",
    (40, 59): "Poor",
    (0, 39): "Critical",
}

# Columns that should not receive blind text/category normalization.
PROTECTED_TEXT_COLUMNS = {
    "email",
    "customer_id",
    "id",
    "uuid",
    "date",
    "created_at",
    "updated_at",
}

EMAIL_COLUMNS = {"email", "e_mail", "email_address"}

MIME_BY_EXTENSION = {
    "csv": {"text/csv", "application/csv", "application/vnd.ms-excel", "text/plain", "application/octet-stream"},
    "xlsx": {
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/octet-stream",
        "application/zip",
    },
    "xls": {
        "application/vnd.ms-excel",
        "application/octet-stream",
    },
}
