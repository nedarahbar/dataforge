"""Download endpoint tests."""

from tests.conftest import upload_sample


def test_clean_file_download(client, sample_csv_bytes):
    uploaded = upload_sample(client, sample_csv_bytes)
    dataset_id = uploaded["dataset_id"]
    client.post(f"/datasets/{dataset_id}/clean", json={})
    response = client.get(f"/datasets/{dataset_id}/download")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "cleaned.csv" in response.headers.get("content-disposition", "")
    assert b"customer_id" in response.content


def test_download_missing_dataset_error(client):
    response = client.get("/datasets/99999/download")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "DATASET_NOT_FOUND"


def test_download_before_cleaning_error(client, sample_csv_bytes):
    uploaded = upload_sample(client, sample_csv_bytes)
    response = client.get(f"/datasets/{uploaded['dataset_id']}/download")
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "DATASET_NOT_CLEANED"
