from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import schemas
from app.database.config import get_db
from app.api.services import data_collection_service

router = APIRouter()

@router.post("/data-collection")
def create_data(data: schemas.DataCollectionCreate, db: Session = Depends(get_db)):
    return data_collection_service.upload_csv_data(db, data)

@router.get("/data-collection")
def get_all_data(db: Session = Depends(get_db)):
    return data_collection_service.get_all_data_collections(db)

@router.get("/data-collection/{id_data}")
def get_data_by_id(id_data: int, db: Session = Depends(get_db)):
    return data_collection_service.get_data_collection_by_id(db, schemas.DataCollectionResponse(id_data=id_data))

@router.delete("/data-collection/{id_data}")
def delete_data_by_id(id_data: int, db: Session = Depends(get_db)):
    return data_collection_service.delete_data_collection(db, id_data)

@router.delete("/data-collection")
def delete_all_data(db: Session = Depends(get_db)):
    return data_collection_service.delete_all_data_collections(db)
