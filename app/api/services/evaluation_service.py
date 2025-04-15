import pandas as pd
from sqlalchemy.orm import Session
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
from app.models import PreprocessedData
from app.constants import EMOTION_LABELS
from app.config import settings
from app.utils.model_handler import load_model
from app.utils.logging_utils import log_error

MODEL_PATH = settings.model_path

def evaluate_model_with_csv(df: pd.DataFrame, db: Session) -> dict:
    try:
        model, vectorizer = load_model(MODEL_PATH)

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

        # Simpan data ke database (opsional tergantung use-case)
        for text, label in zip(X, y_true):
            db.add(PreprocessedData(cleaned_text=text, label=label))
        db.commit()

        return {
            "metrics": metrics,
            "confusion_matrix": matrix_list
        }

    except Exception as e:
        log_error(f"Error in evaluate_model_with_csv: {str(e)}")
        return {
            "metrics": {},
            "confusion_matrix": [],
            "error": "Terjadi kesalahan saat evaluasi model."
        }
