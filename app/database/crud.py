from sqlalchemy.orm import Session
from app.database import schemas
from typing import List, Optional

from app.models import models

# User CRUD
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

# Emotion Label CRUD
def get_emotion_labels(db: Session) -> List[models.EmotionLabel]:
    return db.query(models.EmotionLabel).all()

def create_emotion_label(db: Session, label: schemas.EmotionLabelBase):
    db_label = models.EmotionLabel(name=label.name)
    db.add(db_label)
    db.commit()
    db.refresh(db_label)
    return db_label

# Dataset CRUD
def create_dataset_entry(db: Session, dataset: schemas.DatasetBase):
    db_entry = models.Dataset(text=dataset.text, label_id=dataset.label_id)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_all_datasets(db: Session) -> List[models.Dataset]:
    return db.query(models.Dataset).all()

def delete_dataset(db: Session):
    db.query(models.Dataset).delete()
    db.commit()

# Validation Result CRUD
def create_validation_result(db: Session, result: schemas.ValidationResultBase):
    db_result = models.ValidationResult(
        text=result.text, label_id=result.label_id, 
        accuracy=result.accuracy, precision=result.precision, recall=result.recall
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

def get_validation_results(db: Session) -> List[models.ValidationResult]:
    return db.query(models.ValidationResult).all()
