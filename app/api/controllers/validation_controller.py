from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database.schemas import ValidationResultCreate, ValidationResultResponse
from app.database.connection import get_db
from app.models.validation_model import perform_validation
from app.services.validation_service import (
    get_all_validation_results,
    get_validation_result_by_id,
    delete_all_validation_results,
    get_single_validation_result,
    get_validation_from_csv,
)

router = APIRouter(
    prefix="/validation",
    tags=["Validation"]
)


@router.post("/", response_model=ValidationResultResponse)
def validate_model(payload: ValidationResultCreate, db: Session = Depends(get_db)):
    try:
        return perform_validation(payload, db)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
def read_all_validation_results(db: Session = Depends(get_db)):
    return get_all_validation_results(db)


@router.get("/{validation_id}")
def read_validation_result_by_id(validation_id: int, db: Session = Depends(get_db)):
    result = get_validation_result_by_id(validation_id, db)
    if not result:
        raise HTTPException(status_code=404, detail="Validation result not found")
    return result


@router.delete("/")
def delete_all_validations(db: Session = Depends(get_db)):
    try:
        delete_all_validation_results(db)
        return {"message": "All validation results deleted successfully"}
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/single/{data_id}")
def validate_single_data(data_id: int, db: Session = Depends(get_db)):
    try:
        return get_single_validation_result(data_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/csv")
def validate_from_csv(file: UploadFile, db: Session = Depends(get_db)):
    try:
        return get_validation_from_csv(file, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"CSV validation failed: {str(e)}")
