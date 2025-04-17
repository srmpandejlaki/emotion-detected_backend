from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.database import dataset_controller
from app.database.session import get_db

router = APIRouter(prefix="/data-collection", tags=["Data Collection"])

@router.get("/")
def get_all_data(db: Session = Depends(get_db)):
    return dataset_controller.get_all_data_collection(db)

@router.get("/{id_data}")
def get_data_by_id(id_data: int, db: Session = Depends(get_db)):
    return dataset_controller.get_data_collection_by_id(db, id_data)

@router.post("/")
def create_data(text: str, label_id: Optional[int] = None, db: Session = Depends(get_db)):
    return dataset_controller.create_data_entry(db, text, label_id)

@router.delete("/")
def delete_all_data(db: Session = Depends(get_db)):
    return dataset_controller.delete_all_data_collection(db)
