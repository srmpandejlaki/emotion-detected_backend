from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.services import preprocessing_service
from app.database.session import get_db

router = APIRouter(prefix="/preprocessing", tags=["Preprocessing"])

# Endpoint untuk memproses dan menyimpan semua data preprocessing
@router.post("/process")
def process_and_save_data(db: Session = Depends(get_db)):
    return preprocessing_service.process_and_save_preprocessing(db)

# Endpoint untuk mendapatkan semua hasil preprocessing
@router.get("/all")
def get_all_preprocessed_data(db: Session = Depends(get_db)):
    return preprocessing_service.get_all_preprocessing_results(db)

# Endpoint untuk menambahkan hasil preprocessing secara manual (opsional)
@router.post("/add")
def add_preprocessing_result(id_data: int, text_preprocessing: str, db: Session = Depends(get_db)):
    return preprocessing_service.add_preprocessing_result(db, id_data, text_preprocessing)
