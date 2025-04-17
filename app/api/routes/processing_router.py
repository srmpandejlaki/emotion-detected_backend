from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.api.controllers import processing_controller

router = APIRouter(
    prefix="/processing",
    tags=["Processing"]
)

@router.post("/train")
def train_model_endpoint(ratio: str, db: Session = Depends(get_db)):
    result, error = processing_controller.train_model(ratio, db)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return result
