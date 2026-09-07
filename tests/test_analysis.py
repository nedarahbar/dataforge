"""Analysis endpoint and service tests."""

import pandas as pd

from app.services.analyzer import analyze_dataframe
from tests.conftest import upload_sample


def test_numeric_analysis():
    df = pd.DataFrame({"age": [10, 20, 30], "city": ["A", "B", "A"]})
    result = analyze_dataframe(df, dataset_id=1)
    assert "age" in result.numeric
    assert result.numeric["age"].mean == 20


def test_categorical_analysis():
    df = pd.DataFrame({"city": ["Tehran", "Tehran", "Shiraz"], "age": [1, 2, 3]})
    result = analyze_dataframe(df, dataset_id=1)
    assert result.categorical["city"].unique_count == 2
    assert result.categorical["city"].top_categories[0].value == "Tehran"


def test_business_analysis_when_columns_present():
    df = pd.DataFrame(
        {
            "customer_id": [1, 2, 1],
            "product": ["Laptop", "Phone", "Laptop"],
            "region": ["North", "South", "North"],
            "total_sales": [100.0, 50.0, 80.0],
            "date": ["2026-01-01", "2026-01-15", "2026-02-01"],
        }
    )
    result = analyze_dataframe(df, dataset_id=1)
    assert result.business is not None
    assert result.business.total_sales == 230.0
    assert result.business.top_products is not None


def test_analysis_requires_cleaned_dataset(client, sample_csv_bytes):
    uploaded = upload_sample(client, sample_csv_bytes)
    response = client.get(f"/datasets/{uploaded['dataset_id']}/analysis")
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "DATASET_NOT_CLEANED"


def test_analysis_endpoint_after_cleaning(client, sample_csv_bytes):
    uploaded = upload_sample(client, sample_csv_bytes)
    dataset_id = uploaded["dataset_id"]
    client.post(f"/datasets/{dataset_id}/clean", json={})
    response = client.get(f"/datasets/{dataset_id}/analysis")
    assert response.status_code == 200
    body = response.json()
    assert "numeric" in body
    assert "categorical" in body
