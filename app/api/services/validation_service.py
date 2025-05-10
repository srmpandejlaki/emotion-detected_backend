from typing import List, Union
from app.database.models.model_database import ValidationResult, ValidationData
from app.database.config import SessionLocal
from app.database.schemas import (
    ValidationResultCreate,
    ValidationDataSchema,
    ValidationResponse
)
from sqlalchemy.orm import Session
from app.utils.model_loader import load_model
from app.processing.alternatif_method.bert_lexicon import process_with_bert_lexicon


def classify_text(text: str) -> ValidationResponse:
    model = load_model()
    print("Model loaded:", type(model))  # debug

    if model is None:
        raise ValueError("Model belum tersedia")

    try:
        result = model.predict([text])[0]
    except Exception as e:
        print("Prediction error:", str(e))  # debug
        raise ValueError("Gagal melakukan prediksi. Format model tidak sesuai.")

    if isinstance(result, list):  # Ambiguitas
        result = process_with_bert_lexicon([text])[0]

    return ValidationResponse(text=text, predicted_emotion=result)

def classify_texts(texts: List[str]) -> List[ValidationResponse]:
    model = load_model()
    if model is None:
        raise ValueError("Model belum tersedia")

    results = model.predict(texts)
    final_results = []

    for i, res in enumerate(results):
        if isinstance(res, list):
            resolved = process_with_bert_lexicon([texts[i]])[0]
            final_results.append(ValidationResponse(text=texts[i], predicted_emotion=resolved))
        else:
            final_results.append(ValidationResponse(text=texts[i], predicted_emotion=res))

    return final_results


def save_validation_correctness(data: List[ValidationDataSchema]):
    db: Session = SessionLocal()
    for item in data:
        validation = ValidationData(
            id_process=item.id_process,
            is_correct=item.is_correct
        )
        db.add(validation)
    db.commit()
    db.close()


def save_validation_result(payload: ValidationResultCreate) -> ValidationResult:
    db: Session = SessionLocal()

    result = ValidationResult(
        model_id=payload.model_id,
        accuracy=payload.accuracy,
        matrix_id=payload.matrix_id,
        metrics_id=payload.metrics_id
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    for val in payload.validation_data:
        data = ValidationData(
            id_validation=result.id_validation,
            id_process=val.id_process,
            is_correct=val.is_correct
        )
        db.add(data)

    db.commit()
    db.close()
    return result
