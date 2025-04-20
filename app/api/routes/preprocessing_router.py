from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.database import schemas
from app.api.controllers.preprocessing_controller import (
    create_preprocessing_result_controller,
    get_all_preprocessing_results_controller,
    process_and_save_preprocessing_controller,
    get_process_result_by_id,
    delete_process_result_by_id,
    delete_all_process_result
)

router = APIRouter()

@router.post("/preprocessing_result")
def create_preprocessing_result(id_data: int, text_preprocessing: str, db: Session = Depends(get_db)):
    """
    Menambahkan hasil preprocessing ke dalam database.
    """
    return create_preprocessing_result_controller(id_data, text_preprocessing, db)


@router.get("/preprocessing_result")
def get_preprocessing_results(db: Session = Depends(get_db)):
    """
    Mendapatkan semua hasil preprocessing.
    """
    return get_all_preprocessing_results_controller(db)


@router.post("/process_and_save_preprocessing")
def process_and_save(db: Session = Depends(get_db)):
    """
    Memproses data yang belum dipreprocessing dan menyimpannya.
    """
    return process_and_save_preprocessing_controller(db)


@router.get("/preprocessing_result/{id_process}")
def get_result_by_id(id_process: int, db: Session = Depends(get_db)):
    return get_process_result_by_id(db, schemas.ProcessResult(id_process=id_process))

@router.delete("/preprocessing_result/{id_process}")
def delete_result_by_id(id_process: int, db: Session = Depends(get_db)):
    return delete_process_result_by_id(db, id_process)

@router.delete("/preprocessing_result")
def delete_all_results(db: Session = Depends(get_db)):
    return delete_all_process_result(db)

