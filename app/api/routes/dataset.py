from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database.schemas import DatasetCreate, DatasetResponse
from services.dataset_service import add_dataset_service, get_all_datasets_service

router = APIRouter(prefix="/dataset", tags=["Dataset"])

@router.post("/", response_model=DatasetResponse)
def add_dataset(data: DatasetCreate, db: Session = Depends(get_db)):
    return add_dataset_service(data, db)

@router.get("/", response_model=list[DatasetResponse])
def get_all_datasets(db: Session = Depends(get_db)):
    return get_all_datasets_service(db)
