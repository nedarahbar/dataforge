"""Cleaning pipeline tests."""

import pandas as pd

from app.schemas.cleaning import CleaningConfig
from app.services.cleaner import clean_dataframe
from tests.conftest import upload_sample


def test_cleaner_removes_duplicates():
    df = pd.DataFrame({"a": [1, 1, 2], "b": ["x", "x", "y"]})
    result = clean_dataframe(df, CleaningConfig(fill_missing=False, validate_values=False, detect_outliers=False))
    assert result.duplicates_removed == 1
    assert result.rows_after == 2
    assert result.dataframe.duplicated().sum() == 0


def test_cleaner_fills_numeric_missing_values_with_median():
    df = pd.DataFrame({"age": [10.0, None, 30.0], "city": ["A", "B", "C"]})
    result = clean_dataframe(
        df,
        CleaningConfig(
            remove_duplicates=False,
            normalize_text=False,
            validate_values=False,
            detect_outliers=False,
            numeric_strategy="median",
        ),
    )
    assert result.missing_values_filled == 1
    assert float(result.dataframe.loc[1, "age"]) == 20.0


def test_cleaner_fills_categorical_missing_values_with_mode():
    df = pd.DataFrame({"city": ["Tehran", "Tehran", None], "age": [1, 2, 3]})
    result = clean_dataframe(
        df,
        CleaningConfig(
            remove_duplicates=False,
            normalize_text=False,
            validate_values=False,
            detect_outliers=False,
            categorical_strategy="mode",
        ),
    )
    assert result.missing_values_filled == 1
    assert result.dataframe.loc[2, "city"] == "Tehran"


def test_cleaner_normalizes_text_categories():
    df = pd.DataFrame({"city": ["tehran", "TEHRAN", " Tehran"], "age": [1, 2, 3]})
    result = clean_dataframe(
        df,
        CleaningConfig(
            remove_duplicates=False,
            fill_missing=False,
            validate_values=False,
            detect_outliers=False,
            normalize_text=True,
        ),
    )
    values = set(result.dataframe["city"].tolist())
    assert len(values) == 1
    assert "Tehran" in values


def test_cleaner_detects_invalid_values():
    df = pd.DataFrame({"age": [25, -5, 250], "email": ["a@b.com", "bad", "c@d.com"]})
    result = clean_dataframe(
        df,
        CleaningConfig(
            remove_duplicates=False,
            fill_missing=False,
            normalize_text=False,
            detect_outliers=False,
            validate_values=True,
        ),
    )
    assert result.invalid_values_detected >= 2


def test_cleaner_detects_outliers_with_iqr():
    values = list(range(10, 30)) + [1000]
    df = pd.DataFrame({"sales": values})
    result = clean_dataframe(
        df,
        CleaningConfig(
            remove_duplicates=False,
            fill_missing=False,
            normalize_text=False,
            validate_values=False,
            detect_outliers=True,
        ),
    )
    assert result.outliers_detected >= 1
    # Outliers are reported, not removed
    assert result.rows_after == len(values)


def test_clean_endpoint(client, sample_csv_bytes):
    uploaded = upload_sample(client, sample_csv_bytes)
    response = client.post(
        f"/datasets/{uploaded['dataset_id']}/clean",
        json={
            "remove_duplicates": True,
            "fill_missing": True,
            "normalize_text": True,
            "validate_values": True,
            "detect_outliers": True,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "CLEANED"
    assert body["duplicates_removed"] >= 1
