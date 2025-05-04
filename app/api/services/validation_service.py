from typing import List, Union
from app.database.models.model_database import ValidationResult, ValidationData, ConfusionMatrix, ClassMetrics
from app.database.config import SessionLocal
from app.database.schemas import ValidationResultCreate
from sqlalchemy.orm import Session
from app.utils.model_loader import load_model
from app.processing.alternatif_method.bert_lexicon import process_with_bert_lexicon


def classify_text(text: str) -> str:
    """
    Mengklasifikasikan satu teks menggunakan model Naive Bayes.
    Jika hasil ambigu (dua emosi dengan skor sama), maka diproses dengan BERT+Lexicon.
    """
    model = load_model()
    if model is None:
        return "Model belum tersedia"

    result = model.predict([text])[0]

    if isinstance(result, list):  # Ambiguitas
        result = process_with_bert_lexicon([text])[0]

    return result


def classify_texts(texts: List[str]) -> Union[str, List[str]]:
    """
    Mengklasifikasikan banyak teks.
    Menyelesaikan ambiguitas jika ditemukan.
    """
    model = load_model()
    if model is None:
        return "Model belum tersedia"

    results = model.predict(texts)
    final_results = []

    for i, res in enumerate(results):
        if isinstance(res, list):  # Ambigu
            resolved = process_with_bert_lexicon([texts[i]])[0]
            final_results.append(resolved)
        else:
            final_results.append(res)

    return final_results

def save_validation_data(data: list[dict]):
    db: Session = SessionLocal()
    for item in data:
        validation = ValidationData(
            id_process=item["id_process"],
            is_correct=item["is_correct"]
        )
        db.add(validation)
    db.commit()
    db.close()

def save_validation_result(payload: ValidationResultCreate):
    db: Session = SessionLocal()

    # Simpan hasil utama
    result = ValidationResult(
        model_id=payload.model_id,
        accuracy=payload.accuracy,
        matrix_id=payload.matrix_id,
        metrics_id=payload.metrics_id
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    # Simpan data validasi
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
