from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict

from app.database.config import get_db
from app.api.services import processing_service
from app.database.schemas import (
    UpdateManualLabelRequest,
    UpdatePredictedLabelRequest,
    ProcessingRequest,
    ProcessingResponse
)

def update_manual_emotion_controller(req: UpdateManualLabelRequest, db: Session = Depends(get_db)) -> Dict:
    return processing_service.update_manual_emotion_service(db, req)

def update_predicted_emotion_controller(req: UpdatePredictedLabelRequest, db: Session = Depends(get_db)) -> Dict:
    return processing_service.update_predicted_emotion_service(db, req)

def get_all_processing_data_controller(page: int = 1, limit: int = 10, db: Session = Depends(get_db)) -> Dict:
    return processing_service.get_all_processing_data_service(db, page, limit)

def evaluate_model_controller(req: ProcessingRequest, db: Session = Depends(get_db)) -> ProcessingResponse:
    try:
        ratio = req.ratio_data
        split = ratio.split(":")
        if len(split) != 2:
            raise ValueError
        test_ratio = int(split[1]) / (int(split[0]) + int(split[1]))
    except Exception:
        raise HTTPException(status_code=400, detail="Format rasio tidak valid. Contoh: '70:30'")

    return processing_service.evaluate_model_service(db, test_ratio)

def retrain_model_controller(db: Session = Depends(get_db)) -> Dict:
    return processing_service.retrain_model_service(db)
