"""Database persistence tests."""

from app.database.models import CleaningOperation, Dataset
from app.schemas.cleaning import CleaningConfig
from app.services import dataset_service
from app.utils.constants import DatasetStatus
from tests.conftest import upload_sample


def test_dataset_creation_persisted(client, sample_csv_bytes, db_session):
    uploaded = upload_sample(client, sample_csv_bytes)
    dataset = db_session.get(Dataset, uploaded["dataset_id"])
    assert dataset is not None
    assert dataset.filename == "customers.csv"
    assert dataset.status == DatasetStatus.UPLOADED.value


def test_dataset_retrieval(client, sample_csv_bytes):
    uploaded = upload_sample(client, sample_csv_bytes)
    response = client.get(f"/datasets/{uploaded['dataset_id']}")
    assert response.status_code == 200
    assert response.json()["id"] == uploaded["dataset_id"]


def test_dataset_deletion_removes_record(client, sample_csv_bytes, db_session):
    uploaded = upload_sample(client, sample_csv_bytes)
    dataset_id = uploaded["dataset_id"]
    response = client.delete(f"/datasets/{dataset_id}")
    assert response.status_code == 204
    assert db_session.get(Dataset, dataset_id) is None


def test_cleaning_operation_persistence(client, sample_csv_bytes, db_session):
    uploaded = upload_sample(client, sample_csv_bytes)
    dataset_id = uploaded["dataset_id"]
    client.post(f"/datasets/{dataset_id}/clean", json=CleaningConfig().model_dump())
    ops = db_session.query(CleaningOperation).filter_by(dataset_id=dataset_id).all()
    assert len(ops) == 1
    assert ops[0].rows_before >= ops[0].rows_after


def test_list_datasets_pagination(client, sample_csv_bytes):
    upload_sample(client, sample_csv_bytes)
    upload_sample(client, sample_csv_bytes, filename="second.csv")
    response = client.get("/datasets?page=1&page_size=1")
    assert response.status_code == 200
    body = response.json()
    assert body["page_size"] == 1
    assert body["total"] == 2
    assert len(body["items"]) == 1
