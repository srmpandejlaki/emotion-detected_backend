from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.api.controllers import validation_controller
from app.database.schemas import (
    ValidationSingleInput,
    ValidationBatchInput,
    ValidationDataSchema,
    ValidationResultCreate,
    ValidationResponse,
    TestDataResponse
)

router = APIRouter(prefix="/validation", tags=["Validation"])


@router.post("/classify-single", response_model=ValidationResponse)
def classify_one_text(request: ValidationSingleInput):
    return validation_controller.handle_single_classification(request.text)


@router.get("/testing", response_model=List[TestDataResponse])
def get_unprocessed_test_data(db: Session = Depends(get_db)):
    return validation_controller.fetch_test_data_controller(db)


@router.post("/classify-batch", response_model=List[ValidationResponse])
def classify_many_texts(request: ValidationBatchInput):
    return validation_controller.handle_bulk_classification(request.texts)


@router.post("/save-correctness")
def save_correctness(data: List[ValidationDataSchema]):
    return validation_controller.handle_save_correctness(data)


@router.post("/save-result")
def save_validation_result(payload: ValidationResultCreate):
    return validation_controller.handle_save_validation_result(payload)
