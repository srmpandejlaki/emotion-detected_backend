from fastapi import APIRouter
from typing import List
from app.api.controllers import validation_controller
from app.database.schemas import (
    ValidationSingleInput,
    ValidationBatchInput,
    ValidationDataSchema,
    ValidationResultCreate,
    ValidationResponse
)

router = APIRouter(prefix="/validation", tags=["Validation"])


@router.post("/classify-single", response_model=ValidationResponse)
def classify_one_text(request: ValidationSingleInput):
    return validation_controller.handle_single_classification(request.text)


@router.post("/classify-batch", response_model=List[ValidationResponse])
def classify_many_texts(request: ValidationBatchInput):
    return validation_controller.handle_bulk_classification(request.texts)


@router.post("/save-correctness")
def save_correctness(data: List[ValidationDataSchema]):
    return validation_controller.handle_save_correctness(data)


@router.post("/save-result")
def save_validation_result(payload: ValidationResultCreate):
    return validation_controller.handle_save_validation_result(payload)
