"""Shared pytest fixtures with isolated SQLite DB and storage."""

from __future__ import annotations

import io
from pathlib import Path

import pandas as pd
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import get_settings
from app.database.database import Base, get_db
from app.main import app


@pytest.fixture()
def temp_storage(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    raw = tmp_path / "raw"
    cleaned = tmp_path / "cleaned"
    raw.mkdir()
    cleaned.mkdir()

    get_settings.cache_clear()
    settings = get_settings()
    monkeypatch.setattr(settings, "storage_path", str(tmp_path))
    monkeypatch.setattr(settings, "max_file_size", 1_048_576)
    yield tmp_path
    get_settings.cache_clear()


@pytest.fixture()
def db_session(temp_storage):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session, temp_storage):
    def _override_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def sample_csv_bytes() -> bytes:
    df = pd.DataFrame(
        {
            "customer_id": [1, 2, 2, 3],
            "name": ["Ali", "Sara", "Sara", "Reza"],
            "email": ["a@example.com", "bad-email", "bad-email", None],
            "age": [25, -5, -5, None],
            "city": ["Tehran", "tehran", "tehran", "Shiraz"],
            "region": ["North", "South", "South", "East"],
            "product": ["Laptop", "Phone", "Phone", "Tablet"],
            "quantity": [1, 2, 2, -1],
            "unit_price": [100.0, 50.0, 50.0, 20.0],
            "total_sales": [100.0, 100.0, 100.0, 20.0],
            "date": ["2026-01-01", "01/02/2026", "01/02/2026", "2026/03/10"],
        }
    )
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue()


@pytest.fixture()
def sample_xlsx_bytes() -> bytes:
    df = pd.DataFrame(
        {
            "customer_id": [1, 2],
            "name": ["Ali", "Sara"],
            "email": ["a@example.com", "b@example.com"],
            "age": [30, 40],
            "city": ["Tehran", "Shiraz"],
            "region": ["North", "South"],
            "product": ["Laptop", "Phone"],
            "quantity": [1, 2],
            "unit_price": [100.0, 50.0],
            "total_sales": [100.0, 100.0],
            "date": ["2026-01-01", "2026-02-01"],
        }
    )
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    return buffer.getvalue()


def upload_sample(client: TestClient, content: bytes, filename: str = "customers.csv"):
    response = client.post(
        "/datasets/upload",
        files={"file": (filename, content, "text/csv")},
    )
    assert response.status_code == 201, response.text
    return response.json()
