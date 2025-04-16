from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.api import dataset_controller
from app.database.session import get_db
from app.database.model_database import DataCollection

router = APIRouter(prefix="/data-collection", tags=["Data Collection"])

@router.get("/")
def get_data(db: Session = Depends(get_db)):
    return dataset_controller.get_all_data_collection(db)

@router.get("/{id}", response_model=DataCollection)  # Optional: Tambah response_model untuk validasi response
def get_data_by_id(id: int, db: Session = Depends(get_db)):
    data = dataset_controller.get_data_collection_by_id(db, id)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data

@router.post("/")
def create_data(text: str, label_id: int = None, db: Session = Depends(get_db)):
    return dataset_controller.create_data_entry(db, text, label_id)

@router.delete("/")
def delete_all_data(db: Session = Depends(get_db)):
    dataset_controller.delete_all_data_collection(db)
    return {"message": "All data deleted"}
