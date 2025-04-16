from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from services.preprocessing_service import process_preprocessing, save_preprocessed_data
from typing import List
from app.database import model_database as models

def preprocess_data(db: Session = Depends(get_db)):
    """
    Memproses data teks dari tabel Dataset dan mengembalikan hasil preprocessing.
    """
    try:
        processed = process_preprocessing(db)
        return {"message": "Preprocessing berhasil", "data": processed}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def add_preprocessing_result(db: Session, id_data: int, text_preprocessing: str):
    result = models.ProcessResult(
        id_data=id_data,
        text_preprocessing=text_preprocessing
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result

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

def get_all_preprocessing_results(db: Session) -> List[models.ProcessResult]:
    return db.query(models.ProcessResult).all()