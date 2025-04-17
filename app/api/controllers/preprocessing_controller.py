from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.api.services.preprocessing_service import (
    get_all_preprocessing_results,
    add_preprocessing_result,
    process_and_save_preprocessing
)

def get_all_preprocessing_results_controller(db: Session):
    try:
        # Memanggil service untuk mendapatkan hasil preprocessing
        return get_all_preprocessing_results(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching preprocessing results: {str(e)}")

def create_preprocessing_result_controller(id_data: int, text_preprocessing: str, db: Session):
    try:
        # Memanggil service untuk menambahkan hasil preprocessing
        return add_preprocessing_result(db, id_data, text_preprocessing)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding preprocessing result: {str(e)}")

def process_and_save_preprocessing_controller(db: Session):
    try:
        # Memanggil service untuk memproses data yang belum dipreprocessing
        return process_and_save_preprocessing(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing and saving preprocessing data: {str(e)}")
