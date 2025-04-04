import joblib
import pandas as pd
from sqlalchemy.orm import Session
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
from app.models import PreprocessedData
from app.constants import EMOTION_LABELS
from app.model_service import MODEL_PATH

def evaluate_model_with_csv(df: pd.DataFrame, db: Session) -> dict:
    model, vectorizer = joblib.load(MODEL_PATH)

    X = df["text"]
    y_true = df["label"]
    X_vec = vectorizer.transform(X)
    y_pred = model.predict(X_vec)

    metrics = {
        "accuracy": round(accuracy_score(y_true, y_pred) * 100, 2),
        "precision": round(precision_score(y_true, y_pred, average="macro") * 100, 2),
        "recall": round(recall_score(y_true, y_pred, average="macro") * 100, 2),
    }

    matrix = confusion_matrix(y_true, y_pred, labels=range(1, 8))
    matrix_list = matrix.tolist()

    for text, label in zip(X, y_true):
        new_data = PreprocessedData(cleaned_text=text, label=label)
        db.add(new_data)
    db.commit()

    return {
        "metrics": metrics,
        "confusion_matrix": matrix_list
    }
