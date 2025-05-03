from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api.services import data_collection_service
from app.database import schemas
from app.database.config import get_db

router = APIRouter(
    prefix="/data-collections",
    tags=["Data Collection"]
)

# === GET ALL ===
@router.get("/", response_model=List[schemas.DataCollectionResponse])
def get_all_data_collections(db: Session = Depends(get_db)):
    return data_collection_service.get_all_data_collections(db)

# === GET BY ID ===
@router.get("/{data_id}", response_model=schemas.DataCollectionResponse)
def get_data_collection_by_id(data_id: int, db: Session = Depends(get_db)):
    data = data_collection_service.get_data_collection_by_id(db, data_id)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data

# === CREATE: INPUT MANUAL & CSV ===
@router.post("/", response_model=List[schemas.DataCollectionResponse])
def create_data_collection(
    db: Session = Depends(get_db),
    text_data: Optional[str] = Form(None),
    id_label: Optional[int] = Form(None),
    file: Optional[UploadFile] = File(None),
):
    if file:
        return data_collection_service.create_data_collection(db, file=file)

    if text_data:
        data = schemas.DataCollectionCreate(text_data=text_data, id_label=id_label)
        return data_collection_service.create_data_collection(db, data=data)

    raise HTTPException(status_code=400, detail="Harus mengirimkan file CSV atau input manual")

# === DELETE BY ID ===
@router.delete("/{data_id}")
def delete_data_collection(data_id: int, db: Session = Depends(get_db)):
    data_collection_service.delete_data_collection(db, data_id)
    return {"message": "Data berhasil dihapus"}

# === DELETE ALL ===
@router.delete("/")
def delete_all_data_collections(db: Session = Depends(get_db)):
    data_collection_service.delete_all_data_collections(db)
    return {"message": "Semua data berhasil dihapus"}
