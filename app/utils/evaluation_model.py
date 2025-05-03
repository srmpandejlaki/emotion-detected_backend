from typing import List, Dict, Union
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    confusion_matrix
)

def evaluate_model(
    true_labels: List[str],
    predicted_labels: List[str],
    label_id_mapping: Dict[str, int]  # contoh: {"positive": 1, "negative": 2, ...}
) -> Dict[str, Union[float, List[Dict]]]:

    label_names = list(label_id_mapping.keys())

    # Skor umum
    accuracy = accuracy_score(true_labels, predicted_labels)
    precision = precision_score(true_labels, predicted_labels, average=None, labels=label_names, zero_division=0)
    recall = recall_score(true_labels, predicted_labels, average=None, labels=label_names, zero_division=0)

    # Confusion matrix
    raw_matrix = confusion_matrix(true_labels, predicted_labels, labels=label_names)
    confusion_data = []

    for i, actual_label in enumerate(label_names):
        for j, predicted_label in enumerate(label_names):
            confusion_data.append({
                "label_id": label_id_mapping[actual_label],
                "predicted_label_id": label_id_mapping[predicted_label],
                "total": int(raw_matrix[i][j])
            })

    # Precision dan recall
    precision_recall_data = []
    for i, label in enumerate(label_names):
        precision_recall_data.append({
            "label_id": label_id_mapping[label],
            "precision": float(precision[i]),
            "recall": float(recall[i])
        })

    return {
        "accuracy": float(accuracy),
        "confusion_matrix": confusion_data,
        "precision_recall": precision_recall_data
    }
