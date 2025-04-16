from sqlalchemy.orm import Session
from app.database import schemas
from typing import List, Optional

from app.database import model_database

# User CRUD
def create_user(db: Session, user: schemas.UserCreate):
    db_user = model_database.User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str) -> Optional[model_database.User]:
    return db.query(model_database.User).filter(model_database.User.username == username).first()

# Emotion Label CRUD
def get_emotion_labels(db: Session) -> List[model_database.EmotionLabel]:
    return db.query(model_database.EmotionLabel).all()

def create_emotion_label(db: Session, label: schemas.EmotionLabelBase):
    db_label = model_database.EmotionLabel(name=label.name)
    db.add(db_label)
    db.commit()
    db.refresh(db_label)
    return db_label

# Dataset CRUD
def create_dataset_entry(db: Session, dataset: schemas.DatasetBase):
    db_entry = model_database.Dataset(text=dataset.text, label_id=dataset.label_id)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_all_datasets(db: Session) -> List[model_database.Dataset]:
    return db.query(model_database.Dataset).all()

def delete_dataset(db: Session):
    db.query(model_database.Dataset).delete()
    db.commit()

# Validation Result CRUD
def create_validation_result(db: Session, result: schemas.ValidationResultBase):
    db_result = model_database.ValidationResult(
        text=result.text, label_id=result.label_id, 
        accuracy=result.accuracy, precision=result.precision, recall=result.recall
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

def get_validation_results(db: Session) -> List[model_database.ValidationResult]:
    return db.query(model_database.ValidationResult).all()
