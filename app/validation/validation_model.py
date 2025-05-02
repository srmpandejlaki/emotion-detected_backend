from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score
from sqlalchemy.orm import Session
from app.database.model_database import (
    ValidationResult,
    ValidationData,
    ConfusionMatrix,
    ClassMetrics,
    LabelEmotion,
)

def validate_model_on_test_data(
    db: Session,
    test_texts,
    test_labels,
    predicted_labels,
    id_process_list,
    model_id: int
):
    # Hitung metrik evaluasi
    accuracy = accuracy_score(test_labels, predicted_labels)
    precision = precision_score(test_labels, predicted_labels, average=None, zero_division=0)
    recall = recall_score(test_labels, predicted_labels, average=None, zero_division=0)

    all_labels = sorted(set(test_labels + predicted_labels))
    cm = confusion_matrix(test_labels, predicted_labels, labels=all_labels)

    # Simpan ValidationResult
    validation_result = ValidationResult(
        model_id=model_id,
        accuracy=accuracy,
        matrix_id=None,
        metrics_id=None
    )
    db.add(validation_result)
    db.commit()
    db.refresh(validation_result)

    # Ambil mapping nama label -> id_label
    label_map = {label.nama_label: label.id_label for label in db.query(LabelEmotion).all()}

    # Simpan ConfusionMatrix
    for i, true_label in enumerate(all_labels):
        for j, pred_label in enumerate(all_labels):
            total = cm[i][j]
            db_cm = ConfusionMatrix(
                matrix_id=validation_result.id_validation,
                label_id=label_map.get(true_label),
                predicted_label_id=label_map.get(pred_label),
                total=total
            )
            db.add(db_cm)
    db.commit()

    # Simpan ClassMetrics
    for idx, label in enumerate(all_labels):
        db_metric = ClassMetrics(
            metrics_id=validation_result.id_validation,
            label_id=label_map.get(label),
            precision=precision[idx] if idx < len(precision) else 0.0,
            recall=recall[idx] if idx < len(recall) else 0.0
        )
        db.add(db_metric)
    db.commit()

    # Simpan ValidationData
    for i in range(len(test_texts)):
        is_correct = test_labels[i] == predicted_labels[i]
        val_data = ValidationData(
            id_validation=validation_result.id_validation,
            id_process=id_process_list[i],
            is_correct=is_correct
        )
        db.add(val_data)
    db.commit()

    return {
        "validation_id": validation_result.id_validation,
        "accuracy": accuracy,
        "labels": all_labels
    }
