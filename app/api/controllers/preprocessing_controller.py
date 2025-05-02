from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.api.services import preprocessing_service


def get_all_preprocessing_results_controller(db: Session):
    return preprocessing_service.get_all_preprocessing_results(db)


def get_preprocess_result_by_id_controller(db: Session, process_id: int):
    result = preprocessing_service.get_preprocess_result_by_id(db, process_id)
    if not result:
        raise HTTPException(status_code=404, detail="Preprocessing result not found")
    return result


def preprocessing_and_save_controller(db: Session):
    return preprocessing_service.preprocessing_and_save(db)


def delete_preprocess_result_controller(db: Session, process_id: int):
    return preprocessing_service.delete_preprocess_result(db, process_id)


def delete_all_preprocess_result_controller(db: Session):
    return preprocessing_service.delete_all_preprocess_result(db)
