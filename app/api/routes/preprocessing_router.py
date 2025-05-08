from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.controllers import preprocessing_controller
from app.database.config import get_db

router = APIRouter(
    prefix="/preprocessing", tags=["Preprocessing"]
)

@router.get("/", summary="Ambil semua hasil preprocessing")
def get_all_preprocessing(db: Session = Depends(get_db)):
    return preprocessing_controller.get_all_preprocessing_results_controller(db)

@router.get("/{process_id}", summary="Ambil hasil preprocessing berdasarkan ID")
def get_preprocessing_by_id(process_id: int, db: Session = Depends(get_db)):
    return preprocessing_controller.get_preprocess_result_by_id_controller(db, process_id)

@router.post("/preprocess", summary="Lakukan preprocessing pada data yang belum diproses")
def process_unprocessed_data(db: Session = Depends(get_db)):
    return preprocessing_controller.preprocessing_and_save_controller(db)

@router.delete("/preprocess", summary="Hapus semua hasil preprocessing")
def delete_all_preprocessing(db: Session = Depends(get_db)):
    return preprocessing_controller.delete_all_preprocess_result_controller(db)

@router.delete("/{process_id}", summary="Hapus hasil preprocessing berdasarkan ID")
def delete_preprocessing(process_id: int, db: Session = Depends(get_db)):
    return preprocessing_controller.delete_preprocess_result_controller(db, process_id)

@router.put("/update-label/{id_data}")
def update_label_route(id_data: int, new_label: str, db: Session = Depends(get_db)):
    return preprocessing_controller.update_label_controller(db, id_data, new_label)
