from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import schemas
from app.database.config import get_db
from app.api.services import data_collection_service

router = APIRouter()

# ------------------------- Label Emotion -------------------------
@router.post("/label-emotion")
def create_label(label: schemas.LabelEmotionCreate, db: Session = Depends(get_db)):
    return data_collection_service.create_label_emotion(db, label)

@router.get("/label-emotion")
def get_all_label(db: Session = Depends(get_db)):
    return data_collection_service.get_all_label_emotion(db)

@router.get("/label-emotion/{id_label}")
def get_label_by_id(id_label: int, db: Session = Depends(get_db)):
    return data_collection_service.get_label_emotion_by_id(db, schemas.LabelEmotion(id_label=id_label))


# ------------------------- Data Collection -------------------------
@router.post("/data-collection")
def create_data(data: schemas.DataCollectionCreate, db: Session = Depends(get_db)):
    return data_collection_service.create_data_collection(db, data)

@router.get("/data-collection")
def get_all_data(db: Session = Depends(get_db)):
    return data_collection_service.get_all_data_collections(db)

@router.get("/data-collection/{id_data}")
def get_data_by_id(id_data: int, db: Session = Depends(get_db)):
    return data_collection_service.get_data_collection_by_id(db, schemas.DataCollection(id_data=id_data))

@router.delete("/data-collection/{id_data}")
def delete_data_by_id(id_data: int, db: Session = Depends(get_db)):
    return data_collection_service.delete_data_collection(db, id_data)

@router.delete("/data-collection")
def delete_all_data(db: Session = Depends(get_db)):
    return data_collection_service.delete_all_data_collections(db)
