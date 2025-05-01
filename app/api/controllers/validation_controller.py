from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.validation import validation_service
from app.validation.model_validation import validate_model_on_test_data


def get_unprocessed_data_controller(db: Session):
    return validation_service.get_unprocessed_data(db)


def update_emotion_controller(db: Session, id_process: int, new_emotion: str):
    return validation_service.update_automatic_emotion(db, id_process, new_emotion)


def run_validation_controller(db: Session, test_texts, test_labels, train_texts, train_labels):
    if not (test_texts and test_labels and train_texts and train_labels):
        raise HTTPException(status_code=400, detail="Semua input harus diisi dengan benar.")
    return validate_model_on_test_data(
        db=db,
        test_texts=test_texts,
        test_labels=test_labels,
        train_texts=train_texts,
        train_labels=train_labels
    )