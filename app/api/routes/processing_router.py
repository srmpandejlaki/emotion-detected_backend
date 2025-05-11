from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.orm import Session
from app.api.controllers import processing_controller
from app.database.config import get_db
from app.database.schemas import (
    ProcessingDataListResponse,
    UpdateManualLabelRequest,
    UpdatePredictedLabelRequest,
    EvaluationMetrics,
    MessageResponse
)

router = APIRouter(prefix="/processing", tags=["Processing"])

@router.get("/", response_model=ProcessingDataListResponse)
def get_all_processing_data(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    return processing_controller.get_all_processing_data_controller(db, page, limit)

@router.put("/update-manual", response_model=MessageResponse)
def update_manual_emotion(
    req: UpdateManualLabelRequest,
    db: Session = Depends(get_db)
):
    return processing_controller.update_manual_emotion_controller(db, req)

@router.put("/update-automatic", response_model=MessageResponse)
def update_predicted_emotion(
    req: UpdatePredictedLabelRequest,
    db: Session = Depends(get_db)
):
    return processing_controller.update_predicted_emotion_controller(db, req)

@router.post("/evaluate", response_model=EvaluationMetrics)
def evaluate_model(
    test_size: float = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    return processing_controller.evaluate_model_controller(db, test_size)

@router.post("/retrain", response_model=MessageResponse)
def retrain_model(
    db: Session = Depends(get_db)
):
    return processing_controller.retrain_model_controller(db)
