import os
import joblib
import pandas as pd
from typing import List
from sqlalchemy.orm import Session
from app.models import PreprocessedData
from app.utils import preprocess_text
from app.constants import EMOTION_LABELS

MODEL_PATH = "app/models_ml/naive_bayes_model.pkl"


def predict_single_text(text: str, db: Session) -> str:
    if not os.path.exists(MODEL_PATH):
        return "Model belum tersedia."

    model, vectorizer = joblib.load(MODEL_PATH)
    clean_text = preprocess_text(text)
    vec = vectorizer.transform([clean_text])
    pred = model.predict(vec)[0]

    # Simpan sebagai data latih baru
    new_data = PreprocessedData(cleaned_text=clean_text, label=pred)
    db.add(new_data)
    db.commit()

    return EMOTION_LABELS.get(pred, "tidak diketahui")


def predict_batch_texts(df: pd.DataFrame, db: Session) -> List[dict]:
    if not os.path.exists(MODEL_PATH):
        return []

    model, vectorizer = joblib.load(MODEL_PATH)
    texts = df["text"].tolist()
    clean_texts = [preprocess_text(t) for t in texts]
    vecs = vectorizer.transform(clean_texts)
    preds = model.predict(vecs)

    # Simpan semua ke database
    for text, label in zip(clean_texts, preds):
        db.add(PreprocessedData(cleaned_text=text, label=label))
    db.commit()

    return [
        {"text": orig, "predicted_emotion": EMOTION_LABELS.get(label, "tidak diketahui")}
        for orig, label in zip(texts, preds)
    ]
