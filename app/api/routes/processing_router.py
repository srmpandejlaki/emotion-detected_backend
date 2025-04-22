from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.services.processing_service import train_model, delete_model_by_id
from app.database.config import get_db

router = APIRouter()

# Endpoint untuk melatih model
@router.post("/train_model/{ratio_str}")
def train_model_endpoint(ratio_str: str, db: Session = Depends(get_db)):
    result, error = train_model(ratio_str, db)
    
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    return {
        "model_id": result['model_id'],
        "accuracy": result['accuracy'],
        "precision": result['precision'],
        "recall": result['recall']
    }


# Endpoint untuk menghapus model berdasarkan ID
@router.delete("/delete_model/{model_id}")
def delete_model_endpoint(model_id: int, db: Session = Depends(get_db)):
    success, message = delete_model_by_id(model_id, db)
    
    if not success:
        raise HTTPException(status_code=404, detail=message)
    
    return {"message": message}
