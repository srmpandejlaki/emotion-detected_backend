from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database.model_database import ValidationResult, ValidationData, ProcessResult
from app.classification import naive_bayes_predict
import pandas as pd
from fastapi import UploadFile


def get_all_validation_results(db: Session):
    return db.query(ValidationResult).all()


def get_validation_result_by_id(validation_id: int, db: Session):
    return db.query(ValidationResult).filter_by(id_validation=validation_id).first()


def delete_all_validation_results(db: Session):
    try:
        db.query(ValidationData).delete()
        db.query(ValidationResult).delete()
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise RuntimeError("Failed to delete validation results")


def get_single_validation_result(data_id: int, db: Session):
    data = db.query(ProcessResult).filter_by(id_process=data_id, is_processed=True).first()
    if not data:
        raise ValueError("Data not found or not yet processed")
    
    predicted = naive_bayes_predict(data.text_preprocessing, db)
    return {
        "id_process": data.id_process,
        "text_preprocessing": data.text_preprocessing,
        "automatic_emotion": data.automatic_emotion,
        "predicted_emotion": predicted,
        "is_correct": predicted == data.automatic_emotion
    }


def get_validation_from_csv(file: UploadFile, db: Session):
    df = pd.read_csv(file.file)
    results = []

    for _, row in df.iterrows():
        text = row.get("text_preprocessing")
        true_label = row.get("automatic_emotion")
        if not text or not true_label:
            continue

        predicted = naive_bayes_predict(text, db)
        results.append({
            "text_preprocessing": text,
            "automatic_emotion": true_label,
            "predicted_emotion": predicted,
            "is_correct": predicted == true_label
        })

    return results
