from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers import preprocessing_controller
from app.database.database import get_db

router = APIRouter(prefix="/preprocessing", tags=["Preprocessing"])

@router.get("/")
def get_all_results(db: Session = Depends(get_db)):
    return preprocessing_controller.get_all_preprocessing_results(db)

@router.post("/")
def add_preprocessed(id_data: int, text_preprocessing: str, is_training_data: bool, automatic_label: int = None, db: Session = Depends(get_db)):
    return preprocessing_controller.add_preprocessing_result(db, id_data, text_preprocessing, is_training_data, automatic_label)

router.post("/process")(preprocessing_controller.preprocess_data)
router.post("/save")(preprocessing_controller.save_preprocessed)
