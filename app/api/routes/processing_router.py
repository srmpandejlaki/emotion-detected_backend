from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.config import get_db
from app.api.controllers import processing_controller

router = APIRouter(prefix="/processing", tags=["Processing"])


@router.post("/run")
def run_processing(db: Session = Depends(get_db)):
    return processing_controller.run_processing(db)


@router.get("/evaluate")
def evaluate_model(test_size: float = Query(0.3, ge=0.1, le=0.9), db: Session = Depends(get_db)):
    return processing_controller.evaluate_model(test_size, db)


@router.put("/update/manual-label/{id_process}")
def update_manual_label(id_process: int, new_label: str, db: Session = Depends(get_db)):
    return processing_controller.update_manual_label(id_process, new_label, db)


@router.put("/update/automatic-label/{id_process}")
def update_automatic_label(id_process: int, new_label: str, db: Session = Depends(get_db)):
    return processing_controller.update_automatic_label(id_process, new_label, db)
