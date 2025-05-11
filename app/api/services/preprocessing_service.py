import math
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# httpexception
from fastapi import HTTPException

from app.database.config import SessionLocal
from app.database.models.model_database import DataCollection, ProcessResult
from app.database.schemas import PreprocessingCreate, PreprocessingUpdate
from app.preprocessing.dataset_cleaning import DatasetPreprocessor


def run_preprocessing_for_id(id_data: int):
    """
    Jalankan preprocessing untuk 1 data berdasarkan ID.
    Jika data sudah ada di tabel ProcessResult, maka diupdate.
    Jika belum ada, akan ditambahkan.
    """
    db = SessionLocal()
    try:
        data_entry = db.query(DataCollection).filter(
            DataCollection.id_data == id_data).first()

        if not data_entry:
            raise ValueError(f"Data dengan id_data {id_data} tidak ditemukan.")

        # Persiapkan DataFrame untuk preprocessing
        df_input = pd.DataFrame([{"text": data_entry.text_data}])
        preprocessor = DatasetPreprocessor()
        df_processed = preprocessor.process(df_input)
        preprocessed_text = df_processed["preprocessed_result"].iloc[0]

        existing = db.query(ProcessResult).filter(
            ProcessResult.id_data == id_data).first()
        if existing:
            existing.text_preprocessing = preprocessed_text
            existing.processed_at = datetime.now()
        else:
            new_preprocessing = ProcessResult(
                id_data=id_data,
                text_preprocessing=preprocessed_text,
                is_processed=None,
                automatic_emotion=None,
                processed_at=datetime.now()
            )
            db.add(new_preprocessing)

        db.commit()
        return {"id_data": id_data, "text_preprocessing": preprocessed_text}

    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error: {str(e)}")
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def create_preprocessing_result(db: Session, request: PreprocessingCreate):
    """
    Buat hasil preprocessing berdasarkan permintaan dengan id_data.
    """
    data = db.query(DataCollection).filter(
        DataCollection.id_data == request.id_data).first()
    if not data:
        return None

    df_input = pd.DataFrame([{"text": data.text_data}])
    preprocessor = DatasetPreprocessor()
    df_processed = preprocessor.process(df_input)
    cleaned_text = df_processed["preprocessed_result"].iloc[0]

    new_result = ProcessResult(
        id_data=request.id_data,
        text_preprocessing=cleaned_text,
        is_processed=None,
        automatic_emotion=None,
        processed_at=datetime.now()
    )
    db.add(new_result)
    db.commit()
    db.refresh(new_result)
    return new_result


def get_all_preprocessing_results(db: Session, page: int = 1, limit: int = 10):
    """
    Ambil semua hasil preprocessing dengan pagination.
    """
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
                "id_data": item.data.id_data if item.data else None,
                "text_data": item.data.text_data if item.data else "-",
                "id_label": item.data.id_label if item.data else None,
                "emotion": {
                    "id_label": item.data.emotion.id_label,
                    "emotion_name": item.data.emotion.emotion_name,
                } if item.data and item.data.emotion else None
            }
        })

    return {
        "total_data": total_data,
        "current_page": page,
        "total_pages": total_pages,
        "preprocessing": result
    }


def get_preprocessing_result_by_id(db: Session, id_process: int):
    """
    Ambil 1 data hasil preprocessing berdasarkan id_process.
    """
    return db.query(ProcessResult).filter(ProcessResult.id_process == id_process).first()


def update_preprocessing_result(db: Session, id_process: int, update_data: PreprocessingUpdate):
    """
    Update hasil preprocessing berdasarkan id_process dan update juga data aslinya di data_collection.
    """
    # Cari hasil preprocessing
    process_result = db.query(ProcessResult).filter(
        ProcessResult.id_process == id_process).first()

    if not process_result:
        return None

    # Cari data asli yang terkait
    data_collection = db.query(DataCollection).filter(
        DataCollection.id_data == process_result.id_data).first()

    if not data_collection:
        return None

    try:
        # Update data preprocessing
        if update_data.text_preprocessing is not None:
            process_result.text_preprocessing = update_data.text_preprocessing

        if update_data.automatic_emotion is not None:
            process_result.automatic_emotion = update_data.automatic_emotion
            # Update juga label di data_collection jika diperlukan
            # asumsi automatic_emotion adalah id_label
            data_collection.id_label = update_data.automatic_emotion

        process_result.processed_at = datetime.now()
        db.commit()
        db.refresh(process_result)
        return process_result
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Gagal mengupdate data: {str(e)}"
        )


def delete_preprocessing_result(db: Session, id_process: int):
    """
    Hapus hasil preprocessing berdasarkan id_process beserta data aslinya di data_collection.
    """
    # Cari hasil preprocessing
    process_result = db.query(ProcessResult).filter(
        ProcessResult.id_process == id_process).first()

    if not process_result:
        return None

    # Cari data asli yang terkait
    data_collection = db.query(DataCollection).filter(
        DataCollection.id_data == process_result.id_data).first()

    if not data_collection:
        return None

    try:
        # Hapus data preprocessing terlebih dahulu
        db.delete(process_result)

        # Hapus data asli
        db.delete(data_collection)

        db.commit()
        return {"message": "Data berhasil dihapus dari kedua tabel"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Gagal menghapus data: {str(e)}"
        )
