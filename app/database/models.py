"""ORM models for datasets and cleaning operations."""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.utils.constants import CleaningStatus, DatasetStatus


class Dataset(Base):
    __tablename__ = "datasets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[str] = mapped_column(String(20), nullable=False)
    original_path: Mapped[str] = mapped_column(String(500), nullable=False)
    cleaned_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    rows: Mapped[int] = mapped_column(Integer, default=0)
    columns: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(50), default=DatasetStatus.UPLOADED.value)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    cleaning_operations: Mapped[list["CleaningOperation"]] = relationship(
        "CleaningOperation",
        back_populates="dataset",
        cascade="all, delete-orphan",
    )


class CleaningOperation(Base):
    __tablename__ = "cleaning_operations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    dataset_id: Mapped[int] = mapped_column(ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False)
    configuration: Mapped[str] = mapped_column(Text, nullable=False)
    rows_before: Mapped[int] = mapped_column(Integer, default=0)
    rows_after: Mapped[int] = mapped_column(Integer, default=0)
    duplicates_removed: Mapped[int] = mapped_column(Integer, default=0)
    missing_values_filled: Mapped[int] = mapped_column(Integer, default=0)
    invalid_values_detected: Mapped[int] = mapped_column(Integer, default=0)
    outliers_detected: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(50), default=CleaningStatus.COMPLETED.value)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    dataset: Mapped["Dataset"] = relationship("Dataset", back_populates="cleaning_operations")
