from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.preprocessing_service import process_preprocessing, save_preprocessed_data
from database.database import get_db

router = APIRouter(
    prefix="/preprocessing",
    tags=["Preprocessing"]
)

# Endpoint untuk memulai preprocessing
@router.post("/process")
def process_data(db: Session = Depends(get_db)):
    try:
        # Proses data yang diambil dari database untuk preprocessing
        result = process_preprocessing(db)
        return {"message": "Preprocessing done", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint untuk menyimpan hasil preprocessing
@router.post("/save")
def save_processed_data(data: list, db: Session = Depends(get_db)):
    try:
        # Simpan hasil preprocessing ke database
        saved_data = save_preprocessed_data(data, db)
        return {"message": "Preprocessed data saved", "data": saved_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
