from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.api.services import processing_service

def train_model(ratio: str, db: Session):
    try:
        return processing_service.train_model(ratio, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error get processing_service result: {str(e)}")
