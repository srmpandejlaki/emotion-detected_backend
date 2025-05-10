from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.controllers import preprocessing_controller
from app.database.schemas import PreprocessingCreate, PreprocessingUpdate, PreprocessingResponse
from app.database.config import get_db

router = APIRouter(
    prefix="/preprocessing",
    tags=["Preprocessing"]
)

@router.post("/preprocess", response_model=PreprocessingResponse)
def create_preprocessing(request: PreprocessingCreate, db: Session = Depends(get_db)):
    return preprocessing_controller.create_preprocessing_controller(request, db)

@router.get("/", response_model=list[PreprocessingResponse])
def get_all_preprocessing(db: Session = Depends(get_db)):
    return preprocessing_controller.get_all_preprocessing_controller(db)

@router.get("/{id_process}", response_model=PreprocessingResponse)
def get_preprocessing_by_id(id_process: int, db: Session = Depends(get_db)):
    return preprocessing_controller.get_preprocessing_by_id_controller(id_process, db)

@router.patch("/{id_process}", response_model=PreprocessingResponse)
def update_preprocessing(id_process: int, update_data: PreprocessingUpdate, db: Session = Depends(get_db)):
    return preprocessing_controller.update_preprocessing_controller(id_process, update_data, db)

@router.delete("/{id_process}")
def delete_preprocessing(id_process: int, db: Session = Depends(get_db)):
    return preprocessing_controller.delete_preprocessing_controller(id_process, db)
