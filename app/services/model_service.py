import pandas as pd
from typing import Tuple
from sqlalchemy.orm import Session
from app.models import PreprocessedData
from app.config import settings
from app.utils.model_handler import save_model, is_model_available, load_model
from app.utils.metrics_handler import save_metrics, load_metrics
from app.utils.file_handler import save_test_data
from app.utils.logging_utils import log_error
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score

MODEL_PATH = settings.model_path
TEST_DATA_PATH = settings.test_data_path
METRICS_PATH = settings.metrics_path

def train_model(ratio_str: str, db: Session) -> Tuple[dict, str]:
    data = db.query(PreprocessedData).all()
    if not data:
        return None, "Tidak ada data yang tersedia untuk pelatihan."

    texts = [item.cleaned_text for item in data]
    labels = [item.label for item in data]

    try:
        train_ratio = int(ratio_str.split(":")[0]) / 100
    except ValueError:
        return None, "Format rasio tidak valid. Gunakan format seperti 80:20"

    try:
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=1 - train_ratio, stratify=labels, random_state=42
        )

        vectorizer = CountVectorizer()
        X_train_vec = vectorizer.fit_transform(X_train)
        X_test_vec = vectorizer.transform(X_test)

        model = MultinomialNB()
        model.fit(X_train_vec, y_train)

        # Simpan model dan vectorizer
        save_model(model, vectorizer, MODEL_PATH)

        y_pred = model.predict(X_test_vec)
        metrics = {
            "accuracy": round(accuracy_score(y_test, y_pred) * 100, 2),
            "precision": round(precision_score(y_test, y_pred, average="macro") * 100, 2),
            "recall": round(recall_score(y_test, y_pred, average="macro") * 100, 2),
        }

        # Simpan metrik
        save_metrics(metrics, METRICS_PATH)

        # Simpan data uji
        df_test = pd.DataFrame({
            "text": X_test,
            "label": y_test,
            "predicted": y_pred
        })
        save_test_data(df_test, TEST_DATA_PATH)

        return {"metrics": metrics, "test_data": df_test}, None

    except Exception as e:
        log_error(f"Error in train_model: {str(e)}")
        return None, "Terjadi kesalahan dalam pelatihan model."


def is_model_available() -> bool:
    return is_model_available(MODEL_PATH)


def load_latest_metrics() -> dict:
    return load_metrics(METRICS_PATH)
