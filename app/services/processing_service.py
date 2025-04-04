import os
import joblib
import pandas as pd
from sqlalchemy.orm import Session
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score
from app.models import PreprocessedData

MODEL_PATH = "app/models_ml/naive_bayes_model.pkl"
METRICS_PATH = "app/models_ml/metrics.json"

def train_model(ratio_str: str, db: Session):
    data = db.query(PreprocessedData).all()
    if not data:
        return None, "Tidak ada data untuk pelatihan."

    texts = [d.cleaned_text for d in data]
    labels = [d.label for d in data]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, stratify=labels, random_state=42
    )

    # Training Model
    vectorizer = CountVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    model = MultinomialNB()
    model.fit(X_train_vec, y_train)

    # Simpan Model
    joblib.dump((model, vectorizer), MODEL_PATH)

    # Evaluasi Model
    X_test_vec = vectorizer.transform(X_test)
    y_pred = model.predict(X_test_vec)
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, average="macro"),
        "recall": recall_score(y_test, y_pred, average="macro"),
    }

    # Simpan metrik
    pd.Series(metrics).to_json(METRICS_PATH)
    return metrics, None
