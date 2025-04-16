from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from database.schemas import DatasetCreate, DatasetResponse
from controllers.dataset_controller import handle_add_dataset, handle_get_all_datasets

router = APIRouter(prefix="/dataset", tags=["Dataset"])

@router.post("/", response_model=DatasetResponse)
def add_dataset_route(data: DatasetCreate, db: Session = Depends(get_db)):
    return handle_add_dataset(data, db)

@router.get("/", response_model=list[DatasetResponse])
def get_all_datasets_route(db: Session = Depends(get_db)):
    return handle_get_all_datasets(db)
