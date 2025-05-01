from sqlalchemy.orm import Session
from app.database.model_database import ProcessResult
from typing import List, Dict


def get_unprocessed_data(db: Session) -> List[ProcessResult]:
    """Ambil semua data dengan is_processed == False"""
    return db.query(ProcessResult).filter(ProcessResult.is_processed == False).all()


def update_automatic_emotion(db: Session, id_process: int, new_emotion: str) -> Dict[str, str]:
    """Update kolom automatic_emotion berdasarkan id_process"""
    process = db.query(ProcessResult).filter(ProcessResult.id_process == id_process).first()
    if not process:
        return {"status": "error", "message": "Data not found"}

    process.automatic_emotion = new_emotion
    db.commit()
    return {"status": "success", "message": f"Emotion updated to {new_emotion}"}
