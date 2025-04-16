from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from services.preprocessing_service import process_preprocessing, save_preprocessed_data

def preprocess_data(db: Session = Depends(get_db)):
    """
    Memproses data teks dari tabel Dataset dan mengembalikan hasil preprocessing.
    """
    try:
        processed = process_preprocessing(db)
        return {"message": "Preprocessing berhasil", "data": processed}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def save_preprocessed(db: Session = Depends(get_db)):
    """
    Menyimpan hasil preprocessing ke tabel PreprocessedData.
    """
    try:
        processed = process_preprocessing(db)
        result = save_preprocessed_data(processed, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
