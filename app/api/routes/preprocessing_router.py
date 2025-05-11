from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.controllers import preprocessing_controller as controller
from app.database.schemas import PreprocessingCreate, PreprocessingUpdate, PreprocessingManyRequest
from app.database.config import get_db

router = APIRouter(prefix="/preprocessing", tags=["Preprocessing"])

@router.post("/run/{id_data}")
def run_preprocessing(id_data: int, db: Session = Depends(get_db)):
    return controller.run_preprocessing_by_id_controller(db, id_data)

@router.post("/run-many")
def run_preprocessing_many(request: PreprocessingManyRequest, db: Session = Depends(get_db)):
    return controller.run_preprocessing_many_controller(db, request.id_data_list)

@router.post("/")
def create_preprocessing(request: PreprocessingCreate, db: Session = Depends(get_db)):
    return controller.create_preprocessing_controller(db, request)

@router.get("/")
def get_all_preprocessing(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    return controller.get_all_preprocessing_controller(db, page, limit)

@router.get("/{id_process}")
def get_preprocessing_by_id(id_process: int, db: Session = Depends(get_db)):
    return controller.get_preprocessing_by_id_controller(db, id_process)

@router.put("/{id_process}")
def update_preprocessing(id_process: int, update_data: PreprocessingUpdate, db: Session = Depends(get_db)):
    return controller.update_preprocessing_controller(db, id_process, update_data)

@router.delete("/{id_process}")
def delete_preprocessing(id_process: int, db: Session = Depends(get_db)):
    return controller.delete_preprocessing_controller(db, id_process)
