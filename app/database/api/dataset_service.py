from sqlalchemy.orm import Session
from app.database.model_database import DataCollection

def get_all_data_collection(db: Session):
    return db.query(DataCollection).all()

def create_data_entry(db: Session, text: str, label_id: int = None):
    new_data = DataCollection(text_data=text, label_id=label_id)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data

def get_data_collection_byId(db: Session, id: int):
    return db.query(DataCollection).filter(DataCollection.id == id).first()

def delete_all_data_collection(db: Session):
    db.query(DataCollection).delete()
    db.commit()
