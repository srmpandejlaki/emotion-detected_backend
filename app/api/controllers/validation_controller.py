from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database.config import get_db
from app.database.schemas import ValidationResultResponse, ValidationResultCreate
from app.api.services import validation_service
from app.validation.validation_model import perform_validation

router = APIRouter(prefix="/validation", tags=["Validation"])


@router.post("/run", response_model=ValidationResultResponse)
def run_validation(payload: ValidationResultCreate, db: Session = Depends(get_db)):
    try:
        return perform_validation(payload, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[ValidationResultResponse])
def get_all_validation_results(db: Session = Depends(get_db)):
    results = validation_service.get_all_validation_results(db)
    return [ValidationResultResponse(**res.__dict__) for res in results]


@router.get("/{validation_id}", response_model=ValidationResultResponse)
def get_validation_result_by_id(validation_id: int, db: Session = Depends(get_db)):
    result = validation_service.get_validation_result_by_id(validation_id, db)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Validation result not found")
    return ValidationResultResponse(**result.__dict__)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_validation_results(db: Session = Depends(get_db)):
    validation_service.delete_all_validation_results(db)


@router.get("/single/{data_id}", response_model=Dict[str, Any])
def get_single_validation_result(data_id: int, db: Session = Depends(get_db)):
    try:
        return validation_service.get_single_validation_result(data_id, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/csv", response_model=List[Dict[str, Any]])
def validate_from_csv(file: UploadFile, db: Session = Depends(get_db)):
    return validation_service.get_validation_from_csv(file, db)
