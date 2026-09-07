"""Profiling service and endpoint tests."""

import pandas as pd

from app.services.profiler import profile_dataframe
from tests.conftest import upload_sample


def test_profiler_row_and_column_counts():
    df = pd.DataFrame({"a": [1, 2, None], "b": ["x", "y", "x"]})
    profile = profile_dataframe(df, dataset_id=1)
    assert profile.rows == 3
    assert profile.columns == 2


def test_profiler_missing_and_duplicates():
    df = pd.DataFrame({"a": [1, 1, None], "b": ["x", "x", "y"]})
    profile = profile_dataframe(df, dataset_id=1)
    assert profile.duplicate_rows == 1
    assert profile.total_missing_values == 1


def test_profiler_numeric_statistics():
    df = pd.DataFrame({"age": [10, 20, 30, 40]})
    profile = profile_dataframe(df, dataset_id=1)
    age = profile.columns_profile[0]
    assert age.min == 10
    assert age.max == 40
    assert age.mean == 25


def test_profiler_categorical_unique_count():
    df = pd.DataFrame({"city": ["Tehran", "Shiraz", "Tehran"]})
    profile = profile_dataframe(df, dataset_id=1)
    assert profile.columns_profile[0].unique_count == 2


def test_profile_endpoint(client, sample_csv_bytes):
    uploaded = upload_sample(client, sample_csv_bytes)
    response = client.get(f"/datasets/{uploaded['dataset_id']}/profile")
    assert response.status_code == 200
    body = response.json()
    assert body["rows"] == 4
    assert body["duplicate_rows"] >= 1
    assert "columns_profile" in body
