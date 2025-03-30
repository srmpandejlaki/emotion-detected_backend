from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetCreate, DatasetResponse

router = APIRouter(prefix="/dataset", tags=["Dataset"])

@router.post("/", response_model=DatasetResponse)
def add_dataset(data: DatasetCreate, db: Session = Depends(get_db)):
    new_data = Dataset(text=data.text, label=data.label)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data

@router.get("/", response_model=list[DatasetResponse])
def get_all_datasets(db: Session = Depends(get_db)):
    return db.query(Dataset).all()
