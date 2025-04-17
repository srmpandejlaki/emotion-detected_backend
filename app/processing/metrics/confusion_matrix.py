import numpy as np

def confusion_matrix(y_true, y_pred):
    """
    Menghitung Confusion Matrix
    """
    labels = sorted(list(set(y_true) | set(y_pred)))
    matrix = np.zeros((len(labels), len(labels)), dtype=int)
    
    label_to_index = {label: idx for idx, label in enumerate(labels)}
    
    for true, pred in zip(y_true, y_pred):
        matrix[label_to_index[true]][label_to_index[pred]] += 1
    
    return matrix, labels
