from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.model_database import DataCollection

def get_all_data_collection(db: Session) -> List[DataCollection]:
    return db.query(DataCollection).order_by(DataCollection.id_data.desc()).all()

def create_data_entry(db: Session, text_data: str, label_id: Optional[int] = None) -> DataCollection:
    new_data = DataCollection(text_data=text_data, label_id=label_id)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data

def get_data_collection_by_id(db: Session, id_data: int) -> Optional[DataCollection]:
    return db.query(DataCollection).filter(DataCollection.id_data == id_data).first()

def delete_all_data_collection(db: Session):
    db.query(DataCollection).delete()
    db.commit()
