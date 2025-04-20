from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.api.services.preprocessing_service import (
    get_all_preprocessing_results,
    add_preprocessing_result,
    process_and_save_preprocessing,
    get_preprocess_result_by_id,
    delete_preprocess_result,
    delete_all_preprocess_result
)

def create_preprocessing_result_controller(process_id: int, text_preprocessing: str, db: Session):
    try:
        # Memanggil service untuk menambahkan hasil preprocessing
        return add_preprocessing_result(db, process_id, text_preprocessing)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding preprocessing result: {str(e)}")

def get_all_preprocessing_results_controller(db: Session):
    try:
        # Memanggil service untuk mendapatkan hasil preprocessing
        return get_all_preprocessing_results(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching preprocessing results: {str(e)}")

def process_and_save_preprocessing_controller(db: Session):
    try:
        # Memanggil service untuk memproses data yang belum dipreprocessing
        return process_and_save_preprocessing(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing and saving preprocessing data: {str(e)}")

def get_process_result_by_id_controller(db: Session, process_id: int):
    try:
        return get_preprocess_result_by_id(db, process_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error get preprocessing data: {str(e)}")

def delete_preprocess_result_controller(db: Session, process_id: int):
    try:
        return delete_preprocess_result(db, process_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error delete preprocessing data: {str(e)}")

def delete_all_preprocess_result_controller(db: Session):
    try:
        return delete_all_preprocess_result(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error delete preprocessing data: {str(e)}")
