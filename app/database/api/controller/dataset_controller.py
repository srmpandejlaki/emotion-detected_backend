from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional
from app.database import dataset_service

def get_all_data_collection(db: Session):
    return dataset_service.get_all_data_collection(db)

def get_data_collection_by_id(db: Session, id_data: int):
    data = dataset_service.get_data_collection_by_id(db, id_data)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data

def create_data_entry(db: Session, text: str, label_id: Optional[int] = None):
    return dataset_service.create_data_entry(db, text, label_id)

def delete_all_data_collection(db: Session):
    dataset_service.delete_all_data_collection(db)
    return {"message": "All data deleted"}
