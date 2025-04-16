from sqlalchemy.orm import Session
from database.models.dataset import Dataset  # pastikan path ini sesuai
from database.schemas import DatasetCreate

def add_dataset_service(data: DatasetCreate, db: Session):
    new_data = Dataset(**data.dict())
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data

def get_all_datasets_service(db: Session):
    return db.query(Dataset).all()
