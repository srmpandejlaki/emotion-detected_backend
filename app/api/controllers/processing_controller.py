from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.api.services import processing_service


router = APIRouter(prefix="/processing", tags=["Processing"])


@router.post("/run")
def run_processing(db: Session = Depends(get_db)):
    texts, labels, id_process_list = processing_service.get_preprocessed_data(db)

    if not texts:
        raise HTTPException(status_code=404, detail="Tidak ada data yang perlu diproses.")

    results = processing_service.process_and_save_predictions_naive_bayes(
        db, texts, labels, id_process_list
    )
    return {"message": "Proses klasifikasi selesai.", "results": results}


@router.get("/evaluate")
def evaluate_model(test_size: float = Query(0.3, ge=0.1, le=0.9), db: Session = Depends(get_db)):
    evaluation = processing_service.evaluate_model(db, test_size)

    if "message" in evaluation:
        raise HTTPException(status_code=404, detail=evaluation["message"])

    return evaluation


@router.put("/update/manual-label/{id_process}")
def update_manual_label(id_process: int, new_label: str, db: Session = Depends(get_db)):
    updated = processing_service.update_manual_emotion_label(db, id_process, new_label)
    if not updated:
        raise HTTPException(status_code=404, detail="Data tidak ditemukan.")
    return {"message": "Label manual berhasil diperbarui."}


@router.put("/update/automatic-label/{id_process}")
def update_automatic_label(id_process: int, new_label: str, db: Session = Depends(get_db)):
    updated = processing_service.update_predicted_emotion_label(db, id_process, new_label)
    if not updated:
        raise HTTPException(status_code=404, detail="Data tidak ditemukan.")
    return {"message": "Label hasil algoritma berhasil diperbarui."}
