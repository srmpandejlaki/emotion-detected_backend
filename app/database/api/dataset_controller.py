from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import model_database as models

def create_data_entry(db: Session, text_data: str, label_id: Optional[int] = None):
    new_data = models.DataCollection(text_data=text_data, label_id=label_id)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data

def get_all_data_collection(db: Session) -> List[models.DataCollection]:
    return db.query(models.DataCollection).order_by(models.DataCollection.id_data.desc()).all()

def get_data_collection_by_id(db: Session, id_data: int) -> Optional[models.DataCollection]:
    return db.query(models.DataCollection).filter(models.DataCollection.id_data == id_data).first()

def delete_all_data_collection(db: Session):
    db.query(models.DataCollection).delete()
    db.commit()
