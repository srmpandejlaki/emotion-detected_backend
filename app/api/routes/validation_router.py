from fastapi import APIRouter, HTTPException, Body
from app.api.controllers import validation_controller
from app.database.schemas import (
    ValidationSingleInput, 
    ValidationBatchInput, 
    ValidationResponse, 
    ValidationResultCreate, 
    ValidationDataSchema,
    ValidationResultResponse
)
from app.api.services import validation_service

router = APIRouter(
    prefix="/validation",
    tags=["Validation"]
)

@router.post("/single", response_model=ValidationResponse)
def classify_single_text(input: ValidationSingleInput):
    result = validation_controller.classify_single_text_controller(input.text)
    if result == "Model belum tersedia":
        raise HTTPException(status_code=404, detail=result)
    return ValidationResponse(text=input.text, predicted_emotion=result)

@router.post("/batch", response_model=list[ValidationResponse])
def classify_dataset(input: ValidationBatchInput):
    try:
        results = validation_controller.classify_dataset_controller(input.texts)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return [
        ValidationResponse(text=text, predicted_emotion=emotion)
        for text, emotion in zip(input.texts, results)
    ]


@router.post("/save")
def save_validation_data(data: list[ValidationDataSchema]):
    validation_service.save_validation_data([d.dict() for d in data])
    return {"message": "Validation data saved successfully."}

@router.post("/evaluate", response_model=ValidationResultResponse)
def evaluate_validation(payload: ValidationResultCreate):
    result = validation_service.save_validation_result(payload)
    return result

