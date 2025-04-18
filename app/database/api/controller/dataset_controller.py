from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional
from app.database import model_database
from app.database import schemas


# ---------- Label Emotion ----------
def create_label_emotion(db: Session, label: schemas.LabelEmotionCreate):
    db_label = model_database.LabelEmotion(**label.dict())
    db.add(db_label)
    db.commit()
    db.refresh(db_label)
    return db_label

def get_all_label_emotion(db: Session):
    return db.query(model_database.LabelEmotion).all()


# ---------- Data Collection ----------
def create_data_collection(db: Session, data: schemas.DataCollectionCreate):
    db_data = model_database.DataCollection(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def get_all_data_collection(db: Session):
    return db.query(model_database.DataCollection).all()

def delete_all_data_collection(db: Session):
    db.query(model_database.DataCollection).delete()
    db.commit()


# ---------- Process Result ----------
def create_process_result(db: Session, result: schemas.ProcessResultCreate):
    db_result = model_database.ProcessResult(**result.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

def get_all_process_result(db: Session):
    return db.query(model_database.ProcessResult).all()

def delete_all_process_result(db: Session):
    db.query(model_database.ProcessResult).delete()
    db.commit()


# ---------- Model ----------
def create_model(db: Session, model: schemas.ModelCreate):
    db_model = model_database.Model(**model.dict())
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

def get_all_model(db: Session):
    return db.query(model_database.Model).all()


# ---------- Model Data ----------
def create_model_data(db: Session, data: schemas.ModelDataCreate):
    db_data = model_database.ModelData(**data.dict())
    db.add(db_data)
    db.commit()
    return db_data

def get_all_model_data(db: Session):
    return db.query(model_database.ModelData).all()


# ---------- Validation Result ----------
def create_validation_result(db: Session, result: schemas.ValidationResultCreate):
    db_result = model_database.ValidationResult(**result.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

def get_all_validation_result(db: Session):
    return db.query(model_database.ValidationResult).all()


# ---------- Validation Data ----------
def create_validation_data(db: Session, data: schemas.ValidationDataCreate):
    db_data = model_database.ValidationData(**data.dict())
    db.add(db_data)
    db.commit()
    return db_data

def get_all_validation_data(db: Session):
    return db.query(model_database.ValidationData).all()


# ---------- Confusion Matrix ----------
def create_confusion_matrix(db: Session, matrix: schemas.ConfusionMatrixCreate):
    db_matrix = model_database.ConfusionMatrix(**matrix.dict())
    db.add(db_matrix)
    db.commit()
    return db_matrix

def get_all_confusion_matrix(db: Session):
    return db.query(model_database.ConfusionMatrix).all()


# ---------- Class Metrics ----------
def create_class_metrics(db: Session, metric: schemas.ClassMetricsCreate):
    db_metric = model_database.ClassMetrics(**metric.dict())
    db.add(db_metric)
    db.commit()
    return db_metric

def get_all_class_metrics(db: Session):
    return db.query(model_database.ClassMetrics).all()
