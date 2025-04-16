from fastapi import HTTPException
from sqlalchemy.orm import Session
from database.schemas import DatasetCreate
from services.dataset_service import add_dataset_service, get_all_datasets_service

def handle_add_dataset(data: DatasetCreate, db: Session):
    result = add_dataset_service(data, db)
    if not result:
        raise HTTPException(status_code=400, detail="Gagal menambahkan dataset.")
    return result

def handle_get_all_datasets(db: Session):
    return get_all_datasets_service(db)
