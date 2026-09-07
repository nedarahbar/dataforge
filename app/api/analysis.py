"""Analysis-focused routes (re-exported under /analysis for clarity)."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.analysis import AnalysisResponse
from app.services import dataset_service

router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.get(
    "/datasets/{dataset_id}",
    response_model=AnalysisResponse,
    summary="Analyze a cleaned dataset",
)
def analyze_dataset(dataset_id: int, db: Session = Depends(get_db)) -> AnalysisResponse:
    return dataset_service.analyze_dataset(db, dataset_id)
