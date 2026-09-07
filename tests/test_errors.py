"""API error contract tests."""


def test_404_dataset_not_found(client):
    response = client.get("/datasets/123456")
    assert response.status_code == 404
    body = response.json()
    assert body["error"]["code"] == "DATASET_NOT_FOUND"


def test_422_invalid_cleaning_payload(client, sample_csv_bytes):
    uploaded = client.post(
        "/datasets/upload",
        files={"file": ("customers.csv", sample_csv_bytes, "text/csv")},
    ).json()
    response = client.post(
        f"/datasets/{uploaded['dataset_id']}/clean",
        json={"numeric_strategy": "not-a-strategy"},
    )
    assert response.status_code == 422
    assert "error" in response.json()


def test_400_dataset_not_cleaned(client, sample_csv_bytes):
    uploaded = client.post(
        "/datasets/upload",
        files={"file": ("customers.csv", sample_csv_bytes, "text/csv")},
    ).json()
    response = client.get(f"/datasets/{uploaded['dataset_id']}/quality")
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "DATASET_NOT_CLEANED"


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
