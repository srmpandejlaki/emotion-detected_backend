from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.services import data_collection_service
from app.database import schemas
from app.database.config import get_db

router = APIRouter(
    prefix="/dataset",
    tags=["Data Collection"]
)


# ✅ Get all data collections (dengan pagination)
@router.get("/", response_model=dict)
def get_all_data_collections(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    return data_collection_service.get_all_data_collections(db, page, limit)


# ✅ Get one by ID
@router.get("/{data_id}", response_model=schemas.DataCollection)
def get_data_collection_by_id(data_id: int, db: Session = Depends(get_db)):
    data = data_collection_service.get_data_collection_by_id(db, data_id)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data


# ✅ Create manual entry
@router.post("/manual", response_model=List[schemas.DataCollection])
def create_data_manual(data: schemas.DataCollectionCreate, db: Session = Depends(get_db)):
    return data_collection_service.create_data_collection(db=db, data=data)


# ✅ Upload via CSV
@router.post("/csv", response_model=List[schemas.DataCollection])
def upload_csv_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return data_collection_service.create_data_collection(db=db, file=file)


# ✅ Delete single data
@router.delete("/{data_id}")
def delete_data(data_id: int, db: Session = Depends(get_db)):
    data_collection_service.delete_data_collection(db, data_id)
    return {"message": "Data berhasil dihapus"}


# ✅ Delete all data
@router.delete("/delete-all")
def delete_all_data(db: Session = Depends(get_db)):
    data_collection_service.delete_all_data_collections(db)
    return {"message": "Semua data berhasil dihapus"}
