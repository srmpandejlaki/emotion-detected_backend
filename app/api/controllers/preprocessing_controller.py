from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.api.services import preprocessing_service
from app.database.schemas import PreprocessingCreate, PreprocessingUpdate

def create_preprocessing_controller(request: PreprocessingCreate, db: Session = Depends(get_db)):
    result = preprocessing_service.create_preprocessing_result(db, request)
    if not result:
        raise HTTPException(status_code=404, detail="DataCollection not found")
    return result

def get_all_preprocessing_controller(db: Session = Depends(get_db)):
    return preprocessing_service.get_all_preprocessing_results(db)

def get_preprocessing_by_id_controller(id_process: int, db: Session = Depends(get_db)):
    result = preprocessing_service.get_preprocessing_result_by_id(db, id_process)
    if not result:
        raise HTTPException(status_code=404, detail="Preprocessing result not found")
    return result

def update_preprocessing_controller(id_process: int, update_data: PreprocessingUpdate, db: Session = Depends(get_db)):
    updated = preprocessing_service.update_preprocessing_result(db, id_process, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Data not found")
    return updated

def delete_preprocessing_controller(id_process: int, db: Session = Depends(get_db)):
    deleted = preprocessing_service.delete_preprocessing_result(db, id_process)
    if not deleted:
        raise HTTPException(status_code=404, detail="Data not found")
    return {"message": f"Data with id_process {id_process} has been deleted"}
