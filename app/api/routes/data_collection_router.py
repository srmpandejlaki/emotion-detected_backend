from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.api.controllers import data_collection_controller
from app.database import schemas
from app.database.config import get_db

router = APIRouter(
    prefix="/dataset",
    tags=["Data Collection"]
)

# ✅ Get all data collections (dengan pagination)
@router.get("/list", response_model=dict)
def get_all_data_collections(db: Session = Depends(get_db), page: int = 1, limit: int = 10):
    return data_collection_controller.get_all_data_collections_controller(db=db, page=page, limit=limit)

# ✅ Get one by ID
@router.get("/{data_id}", response_model=schemas.DataCollection)
def get_data_collection_by_id(data_id: int, db: Session = Depends(get_db)):
    return data_collection_controller.get_data_collection_by_id_controller(db=db, data_id=data_id)

# ✅ Create manual entry
@router.post("/manual", response_model=List[schemas.DataCollection])
def create_data_manual(data: schemas.DataCollectionCreate, db: Session = Depends(get_db)):
    return data_collection_controller.create_data_collection_manual_controller(db=db, data=data)

# ✅ Upload via CSV
@router.post("/csv", response_model=List[schemas.DataCollection])
def upload_csv_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return data_collection_controller.upload_csv_file_controller(db=db, file=file)

# ✅ Delete single data
@router.delete("/{data_id}")
def delete_data(data_id: int, db: Session = Depends(get_db)):
    return data_collection_controller.delete_data_collection_controller(db=db, data_id=data_id)

# ✅ Delete all data
@router.delete("/delete-all")
def delete_all_data(db: Session = Depends(get_db)):
    return data_collection_controller.delete_all_data_collections_controller(db=db)
