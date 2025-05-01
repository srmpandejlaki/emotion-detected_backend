from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.services.validation_service import validation_service
from app.validation.validation import validate_model_on_test_data
from app.database.schemas.validation_schema import ValidationInput, UpdateEmotionInput


def get_unprocessed_data_controller(db: Session):
    return validation_service.get_unprocessed_data(db)


def update_emotion_controller(db: Session, data: UpdateEmotionInput):
    return validation_service.update_automatic_emotion(db, data.id_process, data.new_emotion)


def run_validation_controller(db: Session, input_data: ValidationInput):
    if not (input_data.test_texts and input_data.test_labels and input_data.train_texts and input_data.train_labels):
        raise HTTPException(status_code=400, detail="Semua input harus diisi dengan benar.")
    
    result = validate_model_on_test_data(
        db=db,
        test_texts=input_data.test_texts,
        test_labels=input_data.test_labels,
        train_texts=input_data.train_texts,
        train_labels=input_data.train_labels
    )
    return result
