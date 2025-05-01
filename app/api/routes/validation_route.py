from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.api.controllers import validation_controller

router = APIRouter(prefix="/validation", tags=["Validation"])


@router.get("/unprocessed")
def get_unprocessed_data(db: Session = Depends(get_db)):
    return validation_controller.get_unprocessed_data_controller(db)


@router.post("/update-emotion")
def update_emotion(id_process: int, new_emotion: str, db: Session = Depends(get_db)):
    return validation_controller.update_emotion_controller(db, id_process, new_emotion)


@router.post("/run")
def run_validation(
    test_texts: list[str],
    test_labels: list[str],
    train_texts: list[str],
    train_labels: list[str],
    db: Session = Depends(get_db)
):
    return validation_controller.run_validation_controller(
        db, test_texts, test_labels, train_texts, train_labels
    )
