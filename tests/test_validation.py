"""Validation and unsupported file tests."""

import pandas as pd

from app.services.validator import count_invalid_values, is_valid_email, summarize_invalid_values


def test_invalid_age_detected():
    df = pd.DataFrame({"age": [25, -5, 250, 40]})
    summary = summarize_invalid_values(df)
    assert summary["age"] == 2


def test_invalid_email_detected():
    assert is_valid_email("valid@example.com")
    assert not is_valid_email("invalid-email")
    df = pd.DataFrame({"email": ["valid@example.com", "invalid-email", None]})
    assert count_invalid_values(df) == 1


def test_unsupported_file_via_api(client, sample_csv_bytes):
    response = client.post(
        "/datasets/upload",
        files={"file": ("data.json", b'{"a":1}', "application/json")},
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "INVALID_FILE_TYPE"
