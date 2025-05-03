from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.services import preprocessing_service
from app.database.config import get_db

router = APIRouter(
    prefix="/preprocessing", tags=["Preprocessing"]
)

@router.get("/", summary="Ambil semua hasil preprocessing")
def get_all_preprocessing(db: Session = Depends(get_db)):
    return preprocessing_service.get_all_preprocessing_results(db)

@router.get("/{process_id}", summary="Ambil hasil preprocessing berdasarkan ID")
def get_preprocessing_by_id(process_id: int, db: Session = Depends(get_db)):
    return preprocessing_service.get_preprocess_result_by_id(db, process_id)

@router.post("/process", summary="Lakukan preprocessing pada data yang belum diproses")
def process_unprocessed_data(db: Session = Depends(get_db)):
    return preprocessing_service.preprocessing_and_save(db)

@router.delete("/{process_id}", summary="Hapus hasil preprocessing berdasarkan ID")
def delete_preprocessing(process_id: int, db: Session = Depends(get_db)):
    return preprocessing_service.delete_preprocess_result(db, process_id)

@router.delete("/", summary="Hapus semua hasil preprocessing")
def delete_all_preprocessing(db: Session = Depends(get_db)):
    return preprocessing_service.delete_all_preprocess_result(db)

@router.put("/update-label/{id_data}")
def update_label_route(id_data: int, new_label: str, db: Session = Depends(get_db)):
    return preprocessing_service.update_label(db, id_data, new_label)

@router.post("/add")
def create_emotion_label(emotion_name: str, db: Session = Depends(get_db)):
    return preprocessing_service.add_emotion_label(db, emotion_name)
