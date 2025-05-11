from sqlalchemy.orm import Session
from app.api.services.processing_service import (
    get_all_processing_data,
    update_manual_emotion,
    update_predicted_emotion,
    evaluate_model,
    retrain_model
)
from app.database.schemas import (
    UpdateManualLabelRequest,
    UpdatePredictedLabelRequest,
    EvaluationMetrics,
    ProcessingDataListResponse,
    MessageResponse
)

def get_all_processing_data_controller(db: Session, page: int, limit: int) -> ProcessingDataListResponse:
    return get_all_processing_data(db, page, limit)

def update_manual_emotion_controller(db: Session, req: UpdateManualLabelRequest) -> MessageResponse:
    result = update_manual_emotion(db, req)
    return MessageResponse(message=result["message"])

def update_predicted_emotion_controller(db: Session, req: UpdatePredictedLabelRequest) -> MessageResponse:
    result = update_predicted_emotion(db, req)
    return MessageResponse(message=result["message"])

def evaluate_model_controller(db: Session, test_size: float) -> EvaluationMetrics:
    return evaluate_model(db, test_size)

def retrain_model_controller(db: Session) -> MessageResponse:
    result = retrain_model(db)
    return MessageResponse(message=result["message"])
