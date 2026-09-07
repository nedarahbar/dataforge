"""Quality scoring tests."""

import pandas as pd

from app.services.quality import build_quality_report, calculate_quality_scores
from tests.conftest import upload_sample


def test_quality_score_range():
    dirty = pd.DataFrame({"age": [1, None, 3, 3], "email": ["a@b.com", "bad", "c@d.com", "c@d.com"]})
    score, breakdown = calculate_quality_scores(dirty)
    assert 0 <= score <= 100
    assert 0 <= breakdown.missing_score <= 100
    assert 0 <= breakdown.duplicate_score <= 100


def test_quality_score_improves_after_cleaning():
    before = pd.DataFrame(
        {
            "age": [10, None, 30, 10, None],
            "city": ["Tehran", "tehran", "Tehran", "Tehran", None],
        }
    )
    after = pd.DataFrame(
        {
            "age": [10.0, 20.0, 30.0],
            "city": ["Tehran", "Tehran", "Tehran"],
        }
    )
    before_score, _ = calculate_quality_scores(before)
    after_score, _ = calculate_quality_scores(after)
    assert after_score >= before_score


def test_before_after_quality_report(client, sample_csv_bytes):
    uploaded = upload_sample(client, sample_csv_bytes)
    dataset_id = uploaded["dataset_id"]
    client.post(f"/datasets/{dataset_id}/clean", json={})
    response = client.get(f"/datasets/{dataset_id}/quality")
    assert response.status_code == 200
    body = response.json()
    assert "before" in body and "after" in body
    assert 0 <= body["quality_score"] <= 100
    assert body["after"]["duplicates"] == 0


def test_build_quality_report_direct():
    before = pd.DataFrame({"a": [1, 1, None]})
    after = pd.DataFrame({"a": [1.0, 2.0]})
    report = build_quality_report(1, before, after)
    assert report.dataset_id == 1
    assert report.before.rows == 3
    assert report.after.rows == 2
