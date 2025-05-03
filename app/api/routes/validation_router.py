from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.config import get_db
from app.database.schemas import ValidationResultCreate, ValidationResultResponse
from app.api.services import validation_service

router = APIRouter(
    prefix="/validation",
    tags=["Validation"]
)

# Endpoint untuk melakukan proses validasi model
@router.post("/", response_model=ValidationResultResponse)
def validate_model(payload: ValidationResultCreate, db: Session = Depends(get_db)):
    try:
        result = validation_service.perform_validation(payload, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Endpoint untuk mendapatkan semua hasil validasi
@router.get("/", response_model=List[ValidationResultResponse])
def get_all_validations(db: Session = Depends(get_db)):
    return validation_service.get_all_validation_results(db)


# Endpoint untuk mendapatkan hasil validasi berdasarkan ID
@router.get("/{validation_id}", response_model=ValidationResultResponse)
def get_validation_by_id(validation_id: int, db: Session = Depends(get_db)):
    validation_result = validation_service.get_validation_result_by_id(validation_id, db)
    if not validation_result:
        raise HTTPException(status_code=404, detail="Validation result not found")
    return validation_result


# Endpoint untuk hapus semua hasil validasi
@router.delete("/delete-all")
def delete_all_validations(db: Session = Depends(get_db)):
    validation_service.delete_all_validation_results(db)
    return {"message": "All validation results deleted successfully"}
