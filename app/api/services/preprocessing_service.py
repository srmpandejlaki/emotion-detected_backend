import pandas as pd
import math
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.database.models.model_database import DataCollection, ProcessResult
from app.database.schemas import PreprocessingCreate, PreprocessingUpdate
from app.preprocessing.dataset_cleaning import DatasetPreprocessor  # fungsi preprocessing

from fastapi.encoders import jsonable_encoder
import logging

def create_preprocessing_result(db: Session, request: PreprocessingCreate):
    data = db.query(DataCollection).filter(DataCollection.id_data == request.id_data).first()
    if not data:
        return None

    # Bungkus string ke dalam DataFrame agar cocok dengan input process()
    df_input = pd.DataFrame([{"text": data.text_data}])

    # Proses preprocessing
    preprocessor = DatasetPreprocessor()
    df_processed = preprocessor.process(df_input)

    # Ambil hasil preprocessed pertama (karena hanya 1 baris)
    cleaned_text = df_processed["preprocessed_result"].iloc[0]

    new_result = ProcessResult(
        id_data=request.id_data,
        text_preprocessing=cleaned_text,
        is_processed=None,
        automatic_emotion=None,
        processed_at=None
    )
    db.add(new_result)
    db.commit()
    db.refresh(new_result)
    return new_result

def get_all_preprocessing_results(db: Session, page: int = 1, limit: int = 10):
    total_data = db.query(ProcessResult).count()
    total_pages = math.ceil(total_data / limit) if limit > 0 else 1
    offset = (page - 1) * limit

    data_query = (
        db.query(ProcessResult)
        .order_by(ProcessResult.id_process.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    result = []
    for item in data_query:
        result.append({
            "id_process": item.id_process,
            "id_data": item.id_data,
            "text_preprocessing": item.text_preprocessing,
            "is_processed": item.is_processed,
            "automatic_emotion": item.automatic_emotion,
            "processed_at": item.processed_at,
            "data": {
                "text": item.data.text if item.data else "-",
                "emotion": {
                    "emotion_name": item.data.emotion_name if item.data else "-",
                    "id_label": item.data.id_label if item.data else "-"
                }
            }
        })

    return {
        "total_data": total_data,
        "current_page": page,
        "total_pages": total_pages,
        "preprocessing": result
    }


def get_preprocessing_result_by_id(db: Session, id_process: int):
    return db.query(ProcessResult).filter(ProcessResult.id_process == id_process).first()

def update_preprocessing_result(db: Session, id_process: int, update_data: PreprocessingUpdate):
    result = db.query(ProcessResult).filter(ProcessResult.id_process == id_process).first()
    if not result:
        return None
    if update_data.text_preprocessing is not None:
        result.text_preprocessing = update_data.text_preprocessing
    if update_data.automatic_emotion is not None:
        result.automatic_emotion = update_data.automatic_emotion
    db.commit()
    db.refresh(result)
    return result

def delete_preprocessing_result(db: Session, id_process: int):
    result = db.query(ProcessResult).filter(ProcessResult.id_process == id_process).first()
    if not result:
        return None
    db.delete(result)
    db.commit()
    return result
