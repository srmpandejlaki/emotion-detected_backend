from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score
from app.database.session import Session
from app.database.model_database import ValidationResult, ValidationData, ConfusionMatrix, ClassMetrics, LabelEmotion
from collections import defaultdict


def validate_model_on_test_data(db: Session, test_texts, test_labels, train_texts, train_labels):
    # Dummy prediksi: prediksi = label sama seperti data training pertama (ganti dengan model asli)
    predicted_labels = test_labels  # Ganti dengan hasil model

    accuracy = accuracy_score(test_labels, predicted_labels)
    precision = precision_score(test_labels, predicted_labels, average=None, zero_division=0)
    recall = recall_score(test_labels, predicted_labels, average=None, zero_division=0)
    cm = confusion_matrix(test_labels, predicted_labels, labels=list(set(test_labels + predicted_labels)))

    # Simpan ValidationResult
    validation_result = ValidationResult(model_id=1, accuracy=accuracy)
    db.add(validation_result)
    db.commit()
    db.refresh(validation_result)

    # Simpan ConfusionMatrix
    label_map = {label.nama_label: label.id_label for label in db.query(LabelEmotion).all()}
    for true_idx, true_label in enumerate(set(test_labels + predicted_labels)):
        for pred_idx, pred_label in enumerate(set(test_labels + predicted_labels)):
            total = cm[true_idx][pred_idx]
            db_cm = ConfusionMatrix(
                matrix_id=validation_result.id_validation,
                label_id=label_map.get(true_label),
                predicted_label_id=label_map.get(pred_label),
                total=total
            )
            db.add(db_cm)

    # Simpan ClassMetrics
    for idx, label in enumerate(set(test_labels + predicted_labels)):
        db_metric = ClassMetrics(
            metrics_id=validation_result.id_validation,
            label_id=label_map.get(label),
            precision=precision[idx] if idx < len(precision) else 0.0,
            recall=recall[idx] if idx < len(recall) else 0.0
        )
        db.add(db_metric)

    # Simpan ValidationData
    for i, text in enumerate(test_texts):
        is_correct = test_labels[i] == predicted_labels[i]
        val_data = ValidationData(
            id_validation=validation_result.id_validation,
            id_process=i + 1,  # Placeholder ID
            is_correct=is_correct
        )
        db.add(val_data)

    db.commit()
    return {"accuracy": accuracy, "validation_id": validation_result.id_validation}
