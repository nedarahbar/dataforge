"""Upload endpoint tests."""

from fastapi.testclient import TestClient


def test_valid_csv_upload(client: TestClient, sample_csv_bytes: bytes):
    response = client.post(
        "/datasets/upload",
        files={"file": ("customers.csv", sample_csv_bytes, "text/csv")},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["dataset_id"] > 0
    assert body["file_type"] == "csv"
    assert body["rows"] == 4
    assert body["columns"] == 11
    assert body["status"] == "UPLOADED"


def test_valid_excel_upload(client: TestClient, sample_xlsx_bytes: bytes):
    response = client.post(
        "/datasets/upload",
        files={
            "file": (
                "customers.xlsx",
                sample_xlsx_bytes,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["file_type"] == "xlsx"
    assert body["rows"] == 2


def test_invalid_extension_rejected(client: TestClient):
    response = client.post(
        "/datasets/upload",
        files={"file": ("notes.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "INVALID_FILE_TYPE"


def test_empty_file_rejected(client: TestClient):
    response = client.post(
        "/datasets/upload",
        files={"file": ("empty.csv", b"", "text/csv")},
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "EMPTY_FILE"


def test_file_too_large_rejected(client: TestClient, monkeypatch):
    from app.core.config import get_settings

    settings = get_settings()
    monkeypatch.setattr(settings, "max_file_size", 10)
    response = client.post(
        "/datasets/upload",
        files={"file": ("big.csv", b"a,b\n1,2\n3,4\n", "text/csv")},
    )
    assert response.status_code == 413
    assert response.json()["error"]["code"] == "FILE_TOO_LARGE"


def test_malformed_file_rejected(client: TestClient):
    response = client.post(
        "/datasets/upload",
        files={"file": ("bad.xlsx", b"not-an-excel-file", "application/octet-stream")},
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "INVALID_DATASET"
