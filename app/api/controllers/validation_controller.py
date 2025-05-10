from typing import List
from fastapi import HTTPException
from app.database.schemas import (
    ValidationResultCreate,
    ValidationDataSchema,
    ValidationResponse
)
from app.api.services import validation_service


def handle_single_classification(text: str) -> ValidationResponse:
    try:
        return validation_service.classify_text(text)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


def handle_bulk_classification(texts: List[str]) -> List[ValidationResponse]:
    try:
        return validation_service.classify_texts(texts)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


def handle_save_correctness(data: List[ValidationDataSchema]):
    validation_service.save_validation_correctness(data)
    return {"message": "Data validasi berhasil disimpan."}


def handle_save_validation_result(payload: ValidationResultCreate):
    result = validation_service.save_validation_result(payload)
    return {
        "message": "Hasil validasi berhasil disimpan.",
        "id_validation": result.id_validation
    }
