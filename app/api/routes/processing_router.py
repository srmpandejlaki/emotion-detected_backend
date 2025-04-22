from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.services import processing_service
from app.database.config import get_db

router = APIRouter()

# Endpoint untuk melatih model
def get_unprocessed_data_controller(db: Session):
    try:
        return processing_service.get_unprocessed_data(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def train_model_from_new_data_controller(db: Session):
    try:
        return processing_service.train_from_new_data(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint untuk menghapus model berdasarkan ID
@router.delete("/delete_model/{model_id}")
def delete_model_endpoint(model_id: int, db: Session = Depends(get_db)):
    success, message = processing_service.delete_model_by_id(model_id, db)
    
    if not success:
        raise HTTPException(status_code=404, detail=message)
    
    return {"message": message}
