from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from app.database.model_database import (
    ValidationResult, ValidationData, Model,
    ProcessResult, ConfusionMatrix, ClassMetrics,
    ModelData
)
from app.database.schemas import ValidationResultCreate, ValidationResultResponse
from app.core.classification import naive_bayes_predict
from app.utils.evaluation_model import evaluate_model
from app.utils.label_utils import get_label_id_map


def perform_validation(payload: ValidationResultCreate, db: Session) -> ValidationResultResponse:
    # Ambil model berdasarkan ID
    model = db.query(Model).filter_by(id_model=payload.model_id).first()
    if not model:
        raise ValueError("Model not found")

    # Ambil ID data yang sudah dipakai training
    trained_process_ids = [md.id_process for md in model.model_data]

    # Ambil data uji: yang sudah dipreproses dan belum pernah dipakai training
    test_data = db.query(ProcessResult).filter(
        ProcessResult.is_processed == True,
        ~ProcessResult.id_process.in_(trained_process_ids)
    ).all()

    if not test_data:
        raise ValueError("No validation data available")

    # Proses prediksi dan evaluasi
    true_labels = []
    predicted_labels = []
    correct_flags = []

    for data in test_data:
        predicted = naive_bayes_predict(data.text_preprocessing, db)
        predicted_labels.append(predicted)
        true_label = data.automatic_emotion
        true_labels.append(true_label)
        correct_flags.append(predicted == true_label)

    # Evaluasi model
    evaluation_result = evaluate_model(true_labels, predicted_labels)

    # Mapping label ke ID
    label_id_map = get_label_id_map(db)

    # Simpan confusion matrix & metrics
    new_matrix_id = int(datetime.now().timestamp())
    new_metrics_id = new_matrix_id  # Gunakan ID yang sama untuk keseragaman

    for actual_row in evaluation_result["confusion_matrix"]["matrix"]:
        actual_label = actual_row["actual"]
        actual_id = label_id_map.get(actual_label)
        for predicted_label, total in actual_row.items():
            if predicted_label == "actual":
                continue
            predicted_id = label_id_map.get(predicted_label)
            db.add(ConfusionMatrix(
                matrix_id=new_matrix_id,
                label_id=actual_id,
                predicted_label_id=predicted_id,
                total=total
            ))

    for label, precision in evaluation_result["precision"].items():
        recall = evaluation_result["recall"].get(label, 0.0)
        db.add(ClassMetrics(
            metrics_id=new_metrics_id,
            label_id=label_id_map.get(label),
            precision=precision,
            recall=recall
        ))

    db.flush()

    # Simpan hasil validasi
    validation_result = ValidationResult(
        model_id=payload.model_id,
        accuracy=evaluation_result["accuracy"],
        matrix_id=new_matrix_id,
        metrics_id=new_metrics_id
    )
    db.add(validation_result)
    db.flush()

    # Simpan hasil prediksi masing-masing data
    for idx, data in enumerate(test_data):
        db.add(ValidationData(
            id_validation=validation_result.id_validation,
            id_process=data.id_process,
            is_correct=correct_flags[idx]
        ))

        # Tandai sebagai data training baru
        db.add(ModelData(
            id_model=payload.model_id,
            id_process=data.id_process
        ))

    db.commit()

    return ValidationResultResponse(
        id_validation=validation_result.id_validation,
        model_id=payload.model_id,
        accuracy=validation_result.accuracy,
        matrix_id=validation_result.matrix_id,
        metrics_id=validation_result.metrics_id
    )


def get_all_validation_results(db: Session):
    return db.query(ValidationResult).all()


def get_validation_result_by_id(validation_id: int, db: Session):
    return db.query(ValidationResult).filter_by(id_validation=validation_id).first()


def delete_all_validation_results(db: Session):
    try:
        db.query(ValidationData).delete()
        db.query(ValidationResult).delete()
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise RuntimeError("Failed to delete validation results")
