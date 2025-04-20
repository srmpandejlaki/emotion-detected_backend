from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import crud, schemas
from app.api.dependencies import get_db

router = APIRouter()

# ------------------------- Label Emotion -------------------------
@router.post("/label-emotion")
def create_label(label: schemas.LabelEmotionCreate, db: Session = Depends(get_db)):
    return crud.create_label_emotion(db, label)

@router.get("/label-emotion")
def get_all_label(db: Session = Depends(get_db)):
    return crud.get_all_label_emotion(db)

@router.get("/label-emotion/{id_label}")
def get_label_by_id(id_label: int, db: Session = Depends(get_db)):
    return crud.get_label_emotion_by_id(db, schemas.LabelEmotion(id_label=id_label))


# ------------------------- Data Collection -------------------------
@router.post("/data-collection")
def create_data(data: schemas.DataCollectionCreate, db: Session = Depends(get_db)):
    return crud.create_data_collection(db, data)

@router.get("/data-collection")
def get_all_data(db: Session = Depends(get_db)):
    return crud.get_all_data_collection(db)

@router.get("/data-collection/{id_data}")
def get_data_by_id(id_data: int, db: Session = Depends(get_db)):
    return crud.get_data_collection_by_id(db, schemas.DataCollection(id_data=id_data))

@router.delete("/data-collection/{id_data}")
def delete_data_by_id(id_data: int, db: Session = Depends(get_db)):
    return crud.delete_data_collection_by_id(db, id_data)

@router.delete("/data-collection")
def delete_all_data(db: Session = Depends(get_db)):
    return crud.delete_all_data_collection(db)


# ------------------------- Process Result -------------------------
@router.post("/process-result")
def create_result(result: schemas.ProcessResultCreate, db: Session = Depends(get_db)):
    return crud.create_process_result(db, result)

@router.get("/process-result")
def get_all_results(db: Session = Depends(get_db)):
    return crud.get_all_process_result(db)

@router.get("/process-result/{id_process}")
def get_result_by_id(id_process: int, db: Session = Depends(get_db)):
    return crud.get_process_result_by_id(db, schemas.ProcessResult(id_process=id_process))

@router.delete("/process-result/{id_process}")
def delete_result_by_id(id_process: int, db: Session = Depends(get_db)):
    return crud.delete_process_result_by_id(db, id_process)

@router.delete("/process-result")
def delete_all_results(db: Session = Depends(get_db)):
    return crud.delete_all_process_result(db)


# ------------------------- Model -------------------------
@router.post("/model")
def create_model(model: schemas.ModelCreate, db: Session = Depends(get_db)):
    return crud.create_model(db, model)

@router.get("/model")
def get_all_models(db: Session = Depends(get_db)):
    return crud.get_all_model(db)

@router.get("/model/{id_model}")
def get_model_by_id(id_model: int, db: Session = Depends(get_db)):
    return crud.get_model_by_id(db, schemas.Model(id_model=id_model))

@router.delete("/model/{id_model}")
def delete_model_by_id(id_model: int, db: Session = Depends(get_db)):
    return crud.delete_model_by_id(db, id_model)

@router.delete("/model")
def delete_all_models(db: Session = Depends(get_db)):
    return crud.delete_all_model(db)


# ------------------------- Model Data -------------------------
@router.post("/model-data")
def create_model_data(data: schemas.ModelDataCreate, db: Session = Depends(get_db)):
    return crud.create_model_data(db, data)

@router.get("/model-data")
def get_all_model_data(db: Session = Depends(get_db)):
    return crud.get_all_model_data(db)

@router.get("/model-data/{id_model}/{id_process}")
def get_model_data_by_ids(id_model: int, id_process: int, db: Session = Depends(get_db)):
    return crud.get_model_data_by_id(db, id_model, id_process)

@router.delete("/model-data/{id_model}/{id_process}")
def delete_model_data_by_ids(id_model: int, id_process: int, db: Session = Depends(get_db)):
    return crud.delete_model_data_by_id(db, id_model, id_process)

@router.delete("/model-data")
def delete_all_model_data(db: Session = Depends(get_db)):
    return crud.delete_all_model_data(db)


# ------------------------- Validation Result -------------------------
@router.post("/validation-result")
def create_validation_result(result: schemas.ValidationResultCreate, db: Session = Depends(get_db)):
    return crud.create_validation_result(db, result)

@router.get("/validation-result")
def get_all_validation_result(db: Session = Depends(get_db)):
    return crud.get_all_validation_result(db)

@router.get("/validation-result/{id_validation}")
def get_validation_result_by_id(id_validation: int, db: Session = Depends(get_db)):
    return crud.get_validation_result_by_id(db, schemas.ValidationResult(id_validation=id_validation))

@router.delete("/validation-result/{id_validation}")
def delete_validation_result_by_id(id_validation: int, db: Session = Depends(get_db)):
    return crud.delete_validation_result_by_id(db, id_validation)

@router.delete("/validation-result")
def delete_all_validation_result(db: Session = Depends(get_db)):
    return crud.delete_all_validation_result(db)


# ------------------------- Validation Data -------------------------
@router.post("/validation-data")
def create_validation_data(data: schemas.ValidationDataCreate, db: Session = Depends(get_db)):
    return crud.create_validation_data(db, data)

@router.get("/validation-data")
def get_all_validation_data(db: Session = Depends(get_db)):
    return crud.get_all_validation_data(db)

@router.get("/validation-data/{id_validation}/{id_process}")
def get_validation_data_by_ids(id_validation: int, id_process: int, db: Session = Depends(get_db)):
    return crud.get_validation_data_by_id(db, id_validation, id_process)

@router.delete("/validation-data/{id_validation}/{id_process}")
def delete_validation_data_by_ids(id_validation: int, id_process: int, db: Session = Depends(get_db)):
    return crud.delete_validation_data_by_id(db, id_validation, id_process)

@router.delete("/validation-data")
def delete_all_validation_data(db: Session = Depends(get_db)):
    return crud.delete_all_validation_data(db)


# ------------------------- Confusion Matrix -------------------------
@router.post("/confusion-matrix")
def create_confusion_matrix(matrix: schemas.ConfusionMatrixCreate, db: Session = Depends(get_db)):
    return crud.create_confusion_matrix(db, matrix)

@router.get("/confusion-matrix")
def get_all_confusion_matrix(db: Session = Depends(get_db)):
    return crud.get_all_confusion_matrix(db)

@router.delete("/confusion-matrix/{matrix_id}")
def delete_confusion_matrix_by_id(matrix_id: int, db: Session = Depends(get_db)):
    return crud.delete_confusion_matrix_by_id(db, matrix_id)

@router.delete("/confusion-matrix")
def delete_all_confusion_matrix(db: Session = Depends(get_db)):
    return crud.delete_all_confusion_matrix(db)


# ------------------------- Class Metrics -------------------------
@router.post("/class-metrics")
def create_class_metrics(metric: schemas.ClassMetricsCreate, db: Session = Depends(get_db)):
    return crud.create_class_metrics(db, metric)

@router.get("/class-metrics")
def get_all_class_metrics(db: Session = Depends(get_db)):
    return crud.get_all_class_metrics(db)

@router.delete("/class-metrics/{metrics_id}")
def delete_class_metrics_by_id(metrics_id: int, db: Session = Depends(get_db)):
    return crud.delete_class_metrics_by_id(db, metrics_id)

@router.delete("/class-metrics")
def delete_all_class_metrics(db: Session = Depends(get_db)):
    return crud.delete_all_class_metrics(db)
