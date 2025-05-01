from typing import List, Dict, Union
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    confusion_matrix,
    classification_report
)

def evaluate_model(
    true_labels: List[str],
    predicted_labels: List[str],
    label_names: List[str] = None
) -> Dict[str, Union[float, Dict]]:

    if label_names is None:
        label_names = sorted(list(set(true_labels + predicted_labels)))

    # Skor umum
    accuracy = accuracy_score(true_labels, predicted_labels)
    precision = precision_score(true_labels, predicted_labels, average=None, labels=label_names, zero_division=0)
    recall = recall_score(true_labels, predicted_labels, average=None, labels=label_names, zero_division=0)

    # Confusion matrix mentah
    matrix = confusion_matrix(true_labels, predicted_labels, labels=label_names)

    # Susun dalam bentuk tabel detail
    detailed_conf_matrix = []
    for i, actual in enumerate(label_names):
        row = {"actual": actual}
        for j, predicted in enumerate(label_names):
            row[predicted] = int(matrix[i][j])
        detailed_conf_matrix.append(row)

    result = {
        "accuracy": accuracy,
        "precision": dict(zip(label_names, precision)),
        "recall": dict(zip(label_names, recall)),
        "confusion_matrix": {
            "labels": label_names,
            "matrix": detailed_conf_matrix
        },
        "classification_report": classification_report(true_labels, predicted_labels, labels=label_names, zero_division=0, output_dict=True)
    }

    return result
