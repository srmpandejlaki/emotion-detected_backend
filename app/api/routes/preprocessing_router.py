from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.preprocessing_controller import (
    get_all_preprocessing_results_controller,
    create_preprocessing_result_controller,
    process_and_save_preprocessing_controller
)

router = APIRouter()

@router.get("/preprocessing_results")
def get_preprocessing_results(db: Session = Depends(get_db)):
    """
    Mendapatkan semua hasil preprocessing.
    """
    return get_all_preprocessing_results_controller(db)


@router.post("/preprocessing_result")
def create_preprocessing_result(id_data: int, text_preprocessing: str, db: Session = Depends(get_db)):
    """
    Menambahkan hasil preprocessing ke dalam database.
    """
    return create_preprocessing_result_controller(id_data, text_preprocessing, db)


@router.post("/process_and_save_preprocessing")
def process_and_save(db: Session = Depends(get_db)):
    """
    Memproses data yang belum dipreprocessing dan menyimpannya.
    """
    return process_and_save_preprocessing_controller(db)
