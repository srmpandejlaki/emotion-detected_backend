from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Dict

from app.api.services import processing_service
from app.database.config import get_db

router = APIRouter(prefix="/processing", tags=["Processing"])


@router.get("/all", response_model=List[Dict])
def get_all_processing_data(db: Session = Depends(get_db)):
    return processing_service.get_all_processing_data(db)


@router.get("/split-dataset", response_model=Dict)
def split_dataset(test_size: float = Query(0.3, ge=0.1, le=0.9), db: Session = Depends(get_db)):
    return processing_service.split_dataset(db, test_size)


@router.get("/evaluate", response_model=Dict)
def evaluate_model(test_size: float = Query(0.3, ge=0.1, le=0.9), db: Session = Depends(get_db)):
    return processing_service.evaluate_model(db, test_size)


@router.post("/predict-naive-bayes", response_model=List[Dict])
def process_with_naive_bayes(
    test_size: float = Query(0.3, ge=0.1, le=0.9), 
    db: Session = Depends(get_db)
):
    texts, labels, ids = processing_service.get_preprocessed_data(db)
    if not texts:
        raise HTTPException(status_code=400, detail="Tidak ada data yang tersedia untuk diproses.")
    return processing_service.process_and_save_predictions_naive_bayes(db, texts, labels, ids, test_size)


@router.put("/update-manual-emotion/{id_process}", response_model=Dict)
def update_manual_emotion(id_process: int, new_label: str, db: Session = Depends(get_db)):
    return processing_service.update_manual_emotion(db, id_process, new_label)


@router.put("/update-predicted-emotion/{id_process}", response_model=Dict)
def update_predicted_emotion(id_process: int, new_label: str, db: Session = Depends(get_db)):
    return processing_service.update_predicted_emotion(db, id_process, new_label)


@router.post("/retrain", response_model=Dict)
def retrain_model(db: Session = Depends(get_db)):
    return processing_service.retrain_model(db)


@router.delete("/delete-all", response_model=Dict)
def delete_all_processing_data(db: Session = Depends(get_db)):
    return processing_service.delete_all_processing(db)
