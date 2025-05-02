from sqlalchemy.orm import Session
from app.database.model_database import ProcessResult


def get_unprocessed_data(db: Session):
    return db.query(ProcessResult).filter(ProcessResult.is_processed == False).all()


def update_automatic_emotion(db: Session, id_process: int, new_emotion: str):
    process = db.query(ProcessResult).filter(ProcessResult.id_process == id_process).first()
    if not process:
        return {"message": "Data tidak ditemukan."}
    process.automatic_label = new_emotion
    db.commit()
    db.refresh(process)
    return process