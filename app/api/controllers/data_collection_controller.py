from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from typing import List

from app.api.services import data_collection_service
from app.database import schemas


def get_all_data_collections_controller(db: Session, page: int = 1, limit: int = 10):
    return data_collection_service.get_all_data_collections(db, page, limit)

def get_data_collection_by_id_controller(db: Session, data_id: int):
    data = data_collection_service.get_data_collection_by_id(db, data_id)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data

def create_data_collection_manual_controller(db: Session, data: schemas.DataCollectionCreate) -> List[schemas.DataCollection]:
    return data_collection_service.create_data_collection(db=db, data=data)

def upload_csv_file_controller(db: Session, file: UploadFile) -> List[schemas.DataCollection]:
    return data_collection_service.create_data_collection(db=db, file=file)

def delete_data_collection_controller(db: Session, data_id: int):
    data_collection_service.delete_data_collection(db, data_id)
    return {"message": "Data berhasil dihapus"}

def delete_all_data_collections_controller(db: Session):
    data_collection_service.delete_all_data_collections(db)
    return {"message": "Semua data berhasil dihapus"}
