from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import schemas
from app.database.config import get_db
from app.api.controllers import data_collection_controller

router = APIRouter(
    prefix="/dataset", tags=["Data Collection"]
)

@router.post("/upload")
def create_data(data: schemas.DataCollectionCreate, db: Session = Depends(get_db)):
    return data_collection_controller.create_data_collection(db, data)

@router.get("/list")
def get_all_data(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
):
    return data_collection_controller.get_all_data_collections(db, page, limit)

@router.get("/{id_data}")
def get_data_by_id(id_data: int, db: Session = Depends(get_db)):
    return data_collection_controller.get_data_collection_by_id(db, id_data)

@router.delete("/{id_data}")
def delete_data_by_id(id_data: int, db: Session = Depends(get_db)):
    return data_collection_controller.delete_data_collection(db, id_data)

@router.delete("/list")
def delete_all_data(db: Session = Depends(get_db)):
    return data_collection_controller.delete_all_data_collections(db)
