from fastapi import APIRouter, Depends
from app.api.controllers import processing_controller
from app.database.schemas import (
    UpdateManualLabelRequest,
    UpdatePredictedLabelRequest,
    ProcessingRequest,
    ProcessingResponse
)

router = APIRouter(
    prefix="/processing",
    tags=["Processing"]
)

@router.post("/update-manual-label")
def update_manual_label(req: UpdateManualLabelRequest):
    return processing_controller.update_manual_emotion_controller(req)

@router.post("/update-predicted-label")
def update_predicted_label(req: UpdatePredictedLabelRequest):
    return processing_controller.update_predicted_emotion_controller(req)

@router.get("/all")
def get_all_processing_data(page: int = 1, limit: int = 10):
    return processing_controller.get_all_processing_data_controller(page, limit)

@router.post("/evaluate", response_model=ProcessingResponse)
def evaluate_model(req: ProcessingRequest):
    return processing_controller.evaluate_model_controller(req)

@router.post("/retrain")
def retrain_model():
    return processing_controller.retrain_model_controller()
