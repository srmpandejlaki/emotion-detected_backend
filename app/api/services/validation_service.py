import os
import pandas as pd
from typing import List
from sqlalchemy.orm import Session
from app.models import PreprocessedData
from app.utils.model_handler import load_model
from app.utils.text_preprocessing import preprocess_text
from app.utils.db_handler import save_preprocessed_data
from app.utils.logging_utils import log_error
from app.constants import EMOTION_LABELS

MODEL_PATH = "app/models_ml/naive_bayes_model.pkl"

def predict_single_text(text: str, db: Session) -> str:
    try:
        model, vectorizer = load_model(MODEL_PATH)
        if model is None or vectorizer is None:
            return "Model belum tersedia."

        clean_text = preprocess_text(text)
        vec = vectorizer.transform([clean_text])
        pred = model.predict(vec)[0]

        # Simpan sebagai data latih baru
        save_preprocessed_data(db, [{"cleaned_text": clean_text, "label": pred}])

        return EMOTION_LABELS.get(pred, "tidak diketahui")

    except Exception as e:
        log_error(f"Error in predict_single_text: {str(e)}")
        return "Terjadi kesalahan dalam prediksi."


def predict_batch_texts(df: pd.DataFrame, db: Session) -> List[dict]:
    try:
        model, vectorizer = load_model(MODEL_PATH)
        if model is None or vectorizer is None:
            return []

        texts = df["text"].tolist()
        clean_texts = [preprocess_text(t) for t in texts]
        vecs = vectorizer.transform(clean_texts)
        preds = model.predict(vecs)

        # Simpan semua ke database
        save_preprocessed_data(db, [{"cleaned_text": t, "label": l} for t, l in zip(clean_texts, preds)])

        return [
            {"text": orig, "predicted_emotion": EMOTION_LABELS.get(label, "tidak diketahui")}
            for orig, label in zip(texts, preds)
        ]

    except Exception as e:
        log_error(f"Error in predict_batch_texts: {str(e)}")
        return []
