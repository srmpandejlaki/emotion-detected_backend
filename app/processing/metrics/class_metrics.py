import numpy as np
import confusion_matrix as confusion_matrix

def accuracy_score(y_true, y_pred):
    """
    Menghitung Akurasi
    """
    matrix, _ = confusion_matrix(y_true, y_pred)
    TP = np.diag(matrix)
    total = np.sum(matrix)
    accuracy = np.sum(TP) / total
    return accuracy

def precision_score(y_true, y_pred, average="macro"):
    """
    Menghitung Precision
    """
    matrix, labels = confusion_matrix(y_true, y_pred)
    precisions = []
    
    for i, label in enumerate(labels):
        TP = matrix[i, i]
        FP = np.sum(matrix[:, i]) - TP
        precision = TP / (TP + FP) if (TP + FP) > 0 else 0
        precisions.append(precision)
    
    if average == "macro":
        return np.mean(precisions)
    return precisions

def recall_score(y_true, y_pred, average="macro"):
    """
    Menghitung Recall
    """
    matrix, labels = confusion_matrix(y_true, y_pred)
    recalls = []
    
    for i, label in enumerate(labels):
        TP = matrix[i, i]
        FN = np.sum(matrix[i, :]) - TP
        recall = TP / (TP + FN) if (TP + FN) > 0 else 0
        recalls.append(recall)
    
    if average == "macro":
        return np.mean(recalls)
    return recalls

