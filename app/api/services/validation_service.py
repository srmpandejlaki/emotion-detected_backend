from sqlalchemy.orm import Session
from app.database.model_database import Processing


def get_unprocessed_data(db: Session):
    return db.query(Processing).filter(Processing.is_processed == False).all()


def update_automatic_emotion(db: Session, id_process: int, new_emotion: str):
    process = db.query(Processing).filter(Processing.id_process == id_process).first()
    if not process:
        return {"message": "Data tidak ditemukan."}
    process.automatic_emotion = new_emotion
    db.commit()
    db.refresh(process)
    return process