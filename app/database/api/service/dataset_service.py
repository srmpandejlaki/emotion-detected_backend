from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.database import model_database
from app.database import schemas

# ---------------- Label Emotion ----------------
def get_all_labels(db: Session):
    return db.query(model_database.LabelEmotion).all()

def get_label_by_id(db: Session, label_id: int):
    return db.query(model_database.LabelEmotion).filter(model_database.LabelEmotion.id_label == label_id).first()

def create_label(db: Session, label: schemas.LabelEmotionCreate):
    db_label = model_database.LabelEmotion(**label.dict())
    db.add(db_label)
    db.commit()
    db.refresh(db_label)
    return db_label


# ---------------- Data Collection ----------------
def get_all_data_collections(db: Session):
    return db.query(model_database.DataCollection).all()

def get_data_collection_by_id(db: Session, data_id: int):
    return db.query(model_database.DataCollection).filter(model_database.DataCollection.id_data == data_id).first()

def create_data_collection(db: Session, data: schemas.DataCollectionCreate):
    db_data = model_database.DataCollection(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def delete_data_collection(db: Session, data_id: int):
    data = get_data_collection_by_id(db, data_id)
    if not data:
        raise HTTPException(status_code=404, detail="Data Collection not found")
    db.delete(data)
    db.commit()

def delete_all_data_collections(db: Session):
    db.query(model_database.DataCollection).delete()
    db.commit()


# ---------------- Process Result ----------------
def get_all_process_results(db: Session):
    return db.query(model_database.ProcessResult).all()

def get_process_result_by_id(db: Session, process_id: int):
    return db.query(model_database.ProcessResult).filter(model_database.ProcessResult.id_process == process_id).first()

def create_process_result(db: Session, process: schemas.ProcessResultCreate):
    db_process = model_database.ProcessResult(**process.dict())
    db.add(db_process)
    db.commit()
    db.refresh(db_process)
    return db_process

def delete_process_result(db: Session, process_id: int):
    process = get_process_result_by_id(db, process_id)
    if not process:
        raise HTTPException(status_code=404, detail="Process Result not found")
    db.delete(process)
    db.commit()

def delete_all_process_result(db: Session):
    db.query(model_database.ProcessResult).delete()
    db.commit()


# ---------------- Model ----------------
def get_all_models(db: Session):
    return db.query(model_database.Model).all()

def get_model_by_id(db: Session, model_id: int):
    return db.query(model_database.Model).filter(model_database.Model.id_model == model_id).first()

def create_model(db: Session, model: schemas.ModelCreate):
    db_model = model_database.Model(**model.dict())
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


# ---------------- Model Data ----------------
def get_all_model_data(db: Session):
    return db.query(model_database.ModelData).all()

def create_model_data(db: Session, model_data: schemas.ModelDataCreate):
    db_model_data = model_database.ModelData(**model_data.dict())
    db.add(db_model_data)
    db.commit()
    return db_model_data


# ---------------- Validation Result ----------------
def get_all_validation_results(db: Session):
    return db.query(model_database.ValidationResult).all()

def get_validation_result_by_id(db: Session, validation_id: int):
    return db.query(model_database.ValidationResult).filter(model_database.ValidationResult.id_validation == validation_id).first()

def create_validation_result(db: Session, validation: schemas.ValidationResultCreate):
    db_validation = model_database.ValidationResult(**validation.dict())
    db.add(db_validation)
    db.commit()
    db.refresh(db_validation)
    return db_validation


# ---------------- Validation Data ----------------
def get_all_validation_data(db: Session):
    return db.query(model_database.ValidationData).all()

def create_validation_data(db: Session, validation_data: schemas.ValidationDataCreate):
    db_validation_data = model_database.ValidationData(**validation_data.dict())
    db.add(db_validation_data)
    db.commit()
    return db_validation_data


# ---------------- Confusion Matrix ----------------
def get_all_confusion_matrix(db: Session):
    return db.query(model_database.ConfusionMatrix).all()

def create_confusion_matrix(db: Session, matrix: schemas.ConfusionMatrixCreate):
    db_matrix = model_database.ConfusionMatrix(**matrix.dict())
    db.add(db_matrix)
    db.commit()
    return db_matrix


# ---------------- Class Metrics ----------------
def get_all_class_metrics(db: Session):
    return db.query(model_database.ClassMetrics).all()

def create_class_metrics(db: Session, metric: schemas.ClassMetricsCreate):
    db_metric = model_database.ClassMetrics(**metric.dict())
    db.add(db_metric)
    db.commit()
    return db_metric
