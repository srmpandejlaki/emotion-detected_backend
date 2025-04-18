from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.api.service import dataset_service
from app.database.config import get_db
from app.database.schemas import schemas

router = APIRouter()


# ---------------- Label Emotion ----------------
@router.get("/label-emotion", response_model=list[schemas.LabelEmotion])
def get_label_emotions(db: Session = Depends(get_db)):
    return dataset_service.get_all_label_emotions(db)

@router.post("/label-emotion", response_model=schemas.LabelEmotion)
def create_label_emotion(label: schemas.LabelEmotionCreate, db: Session = Depends(get_db)):
    return dataset_service.create_label_emotion(db, label)


# ---------------- Data Collection ----------------
@router.get("/data-collection", response_model=list[schemas.DataCollection])
def get_data_collections(db: Session = Depends(get_db)):
    return dataset_service.get_all_data_collections(db)

@router.post("/data-collection", response_model=schemas.DataCollection)
def create_data_collection(data: schemas.DataCollectionCreate, db: Session = Depends(get_db)):
    return dataset_service.create_data_collection(db, data)

@router.delete("/data-collection/{data_id}")
def delete_data_collection(data_id: int, db: Session = Depends(get_db)):
    dataset_service.delete_data_collection(db, data_id)
    return {"message": "Data collection deleted successfully"}

@router.delete("/data-collection")
def delete_all_data_collection(data: int, db: Session = Depends(get_db)):
    dataset_service.delete_all_data_collection(db)
    return {"message": "Data collection deleted successfully"}


# ---------------- Process Result ----------------
@router.get("/process-result", response_model=list[schemas.ProcessResult])
def get_process_results(db: Session = Depends(get_db)):
    return dataset_service.get_all_process_results(db)

@router.post("/process-result", response_model=schemas.ProcessResult)
def create_process_result(result: schemas.ProcessResultCreate, db: Session = Depends(get_db)):
    return dataset_service.create_process_result(db, result)

@router.delete("/process-result/{process_id}")
def delete_process_result(process_id: int, db: Session = Depends(get_db)):
    dataset_service.delete_process_result(db, process_id)
    return {"message": "Process result deleted successfully"}

@router.delete("/process-result/{process_id}")
def delete_process_result(process_id: int, db: Session = Depends(get_db)):
    dataset_service.delete_process_result(db, process_id)
    return {"message": "Process result deleted successfully"}


# ---------------- Model ----------------
@router.get("/model", response_model=list[schemas.Model])
def get_models(db: Session = Depends(get_db)):
    return dataset_service.get_all_models(db)

@router.post("/model", response_model=schemas.Model)
def create_model(model: schemas.ModelCreate, db: Session = Depends(get_db)):
    return dataset_service.create_model(db, model)


# ---------------- Model Data ----------------
@router.get("/model-data", response_model=list[schemas.ModelData])
def get_model_data(db: Session = Depends(get_db)):
    return dataset_service.get_all_model_data(db)

@router.post("/model-data", response_model=schemas.ModelData)
def create_model_data(data: schemas.ModelDataCreate, db: Session = Depends(get_db)):
    return dataset_service.create_model_data(db, data)


# ---------------- Validation Result ----------------
@router.get("/validation-result", response_model=list[schemas.ValidationResult])
def get_validation_results(db: Session = Depends(get_db)):
    return dataset_service.get_all_validation_results(db)

@router.post("/validation-result", response_model=schemas.ValidationResult)
def create_validation_result(result: schemas.ValidationResultCreate, db: Session = Depends(get_db)):
    return dataset_service.create_validation_result(db, result)


# ---------------- Validation Data ----------------
@router.get("/validation-data", response_model=list[schemas.ValidationData])
def get_validation_data(db: Session = Depends(get_db)):
    return dataset_service.get_all_validation_data(db)

@router.post("/validation-data", response_model=schemas.ValidationData)
def create_validation_data(data: schemas.ValidationDataCreate, db: Session = Depends(get_db)):
    return dataset_service.create_validation_data(db, data)


# ---------------- Confusion Matrix ----------------
@router.get("/confusion-matrix", response_model=list[schemas.ConfusionMatrix])
def get_confusion_matrix(db: Session = Depends(get_db)):
    return dataset_service.get_all_confusion_matrix(db)

@router.post("/confusion-matrix", response_model=schemas.ConfusionMatrix)
def create_confusion_matrix(matrix: schemas.ConfusionMatrixCreate, db: Session = Depends(get_db)):
    return dataset_service.create_confusion_matrix(db, matrix)


# ---------------- Class Metrics ----------------
@router.get("/class-metrics", response_model=list[schemas.ClassMetrics])
def get_class_metrics(db: Session = Depends(get_db)):
    return dataset_service.get_all_class_metrics(db)

@router.post("/class-metrics", response_model=schemas.ClassMetrics)
def create_class_metrics(metrics: schemas.ClassMetricsCreate, db: Session = Depends(get_db)):
    return dataset_service.create_class_metrics(db, metrics)
