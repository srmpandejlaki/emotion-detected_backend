from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.database import schemas
from app.api.controllers.preprocessing_controller import (
    create_preprocessing_result_controller,
    get_all_preprocessing_results_controller,
    preprocessing_and_save_controller,
    get_preprocessing_result_by_id_controller,
    delete_preprocessing_result_controller,
    delete_all_preprocessing_result_controller
)

router = APIRouter()

@router.post("/preprocessing")
def create_preprocessing_result(id_data: int, text_preprocessing: str, db: Session = Depends(get_db)):
    """ Menambahkan hasil preprocessing ke dalam database. """
    return create_preprocessing_result_controller(id_data, text_preprocessing, db)


@router.get("/preprocessing")
def get_preprocessing_results(db: Session = Depends(get_db)):
    """ Mendapatkan semua hasil preprocessing. """
    return get_all_preprocessing_results_controller(db)


@router.post("/preprocessing")
def process_and_save(db: Session = Depends(get_db)):
    """ Memproses data yang belum dipreprocessing dan menyimpannya. """
    return preprocessing_and_save_controller(db)


@router.get("/preprocessing/{id_process}")
def get_result_by_id(id_process: int, db: Session = Depends(get_db)):
    return get_preprocessing_result_by_id_controller(db, schemas.ProcessResult(id_process=id_process))

@router.delete("/preprocessing/{id_process}")
def delete_result_by_id(id_process: int, db: Session = Depends(get_db)):
    return delete_preprocessing_result_controller(db, id_process)

@router.delete("/preprocessing")
def delete_all_results(db: Session = Depends(get_db)):
    return delete_all_preprocessing_result_controller(db)

