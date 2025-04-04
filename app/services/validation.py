import joblib
from sqlalchemy.orm import Session
import pandas as pd
from app.models import PreprocessedData
from app.utils import preprocess_text
from app.constants import EMOTION_LABELS
from app.model_service import MODEL_PATH

def predict_single_text(text: str, db: Session) -> str:
    model, vectorizer = joblib.load(MODEL_PATH)
    clean_text = preprocess_text(text)
    vec = vectorizer.transform([clean_text])
    pred = model.predict(vec)[0]

    new_data = PreprocessedData(cleaned_text=clean_text, label=pred)
    db.add(new_data)
    db.commit()

    return EMOTION_LABELS.get(pred, "tidak diketahui")

def predict_batch_texts(df: pd.DataFrame, db: Session):
    model, vectorizer = joblib.load(MODEL_PATH)
    texts = df["text"].tolist()
    clean_texts = [preprocess_text(t) for t in texts]
    vecs = vectorizer.transform(clean_texts)
    preds = model.predict(vecs)

    for text, label in zip(clean_texts, preds):
        db.add(PreprocessedData(cleaned_text=text, label=label))
    db.commit()

    return [
        {"text": orig, "predicted_emotion": EMOTION_LABELS.get(label, "tidak diketahui")}
        for orig, label in zip(texts, preds)
    ]
