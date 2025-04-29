from typing import List, Dict, Union, Optional
from sqlalchemy.orm import Session
from app.processing.algorithm.naive_bayes import classify_text_naive_bayes
from app.database.model_database import ProcessResult

class ProcessingService:
    @staticmethod
    def process_texts(
        db: Session,
        texts: List[str],
        labels: List[str],
        id_process_list: List[int]
    ) -> List[Dict[str, Union[str, int, None, Dict[str, float]]]]:
        return classify_text_naive_bayes(db, texts, labels, id_process_list)

    @staticmethod
    def get_all(db: Session) -> List[ProcessResult]:
        return db.query(ProcessResult).all()

    @staticmethod
    def get_by_id(db: Session, id_process: int) -> Optional[ProcessResult]:
        return db.query(ProcessResult).filter(ProcessResult.id_process == id_process).first()

    @staticmethod
    def delete_all(db: Session):
        db.query(ProcessResult).delete()
        db.commit()

    @staticmethod
    def delete_by_id(db: Session, id_process: int):
        record = db.query(ProcessResult).filter(ProcessResult.id_process == id_process).first()
        if record:
            db.delete(record)
            db.commit()

    @staticmethod
    def save_by_id(
        db: Session,
        id_process: int,
        automatic_emotion: Optional[str]
    ):
        record = db.query(ProcessResult).filter(ProcessResult.id_process == id_process).first()
        if record:
            record.automatic_emotion = automatic_emotion
            record.is_processed = True
            db.commit()

    @staticmethod
    def save_all(
        db: Session,
        data: List[Dict[str, Union[int, Optional[str]]]]
    ):
        for item in data:
            record = db.query(ProcessResult).filter(ProcessResult.id_process == item["id_process"]).first()
            if record:
                record.automatic_emotion = item.get("automatic_emotion")
                record.is_processed = True
        db.commit()
