import os
import joblib
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List, Dict, Tuple
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score

from app.database.model_database import ProcessResult
from app.processing.algorithm.naive_bayes import NaiveBayesClassifier
from app.processing.alternatif_method.bert_lexicon import process_with_bert_lexicon
from app.utils.model_loader import load_model, save_model


MODEL_PATH = os.path.join("app", "model", "naive_bayes_model.pkl")


# Get Process Data from DB
def get_all_processing_data(db: Session) -> List[Dict]:
    return db.query(ProcessResult).all()


def get_preprocessed_data(db: Session) -> Tuple[List[str], List[str], List[int]]:
    results = db.query(ProcessResult).filter(
        ProcessResult.is_processed == False
    ).all()

    texts = [r.text_preprocessing for r in results]
    labels = [r.data.id_label for r in results]
    ids = [r.id_process for r in results]

    return texts, labels, ids


# Dataset Splitting
def _split_dataset(
    texts: List[str],
    labels: List[str],
    ids: List[int],
    test_size: float
) -> Tuple[List[str], List[str], List[int], List[str], List[str], List[int]]:
    return train_test_split(
        texts, labels, ids, test_size=test_size, random_state=42
    )


def split_dataset(db: Session, test_size: float) -> Dict[str, int]:
    texts, labels, ids = get_preprocessed_data(db)
    if not texts:
        return {"message": "Tidak ada data tersedia untuk split."}

    X_train, X_test, y_train, y_test, id_train, id_test = _split_dataset(texts, labels, ids, test_size)

    return {
        "train_count": len(X_train),
        "test_count": len(X_test),
        "total": len(texts)
    }


# Model Evaluation
def evaluate_model(db: Session, test_size: float) -> Dict:
    texts, labels, ids = get_preprocessed_data(db)
    if not texts:
        return {"message": "Tidak ada data yang tersedia untuk evaluasi."}

    X_train, X_test, y_train, y_test, id_train, id_test = _split_dataset(texts, labels, ids, test_size)

    # Latih model
    model = NaiveBayesClassifier()
    model.train(X_train, y_train)
    save_model(model)

    # Prediksi
    predicted = model.predict(X_test)

    all_labels = sorted(set(labels))
    cm = confusion_matrix(y_test, predicted, labels=all_labels)
    precision = precision_score(y_test, predicted, labels=all_labels, average=None, zero_division=0)
    recall = recall_score(y_test, predicted, labels=all_labels, average=None, zero_division=0)
    accuracy = accuracy_score(y_test, predicted)

    return {
        "confusion_matrix": cm.tolist(),
        "accuracy": round(accuracy, 4),
        "precision": {label: round(p, 4) for label, p in zip(all_labels, precision)},
        "recall": {label: round(r, 4) for label, r in zip(all_labels, recall)},
        "labels": all_labels
    }


# Naive Bayes Prediction and Save Results
def process_and_save_predictions_naive_bayes(
    db: Session,
    texts: List[str],
    labels: List[str],
    id_process_list: List[int]
) -> List[Dict]:
    model = load_model()
    if model is None:
        model = NaiveBayesClassifier()
        model.train(texts, labels)
        save_model(model)

    predicted_emotions = model.predict(texts)

    # Hitung probabilitas jika ingin memeriksa emosi ganda (opsional tergantung implementasi)
    data_dua_emosi = model.get_ambiguous_predictions(texts, labels, id_process_list)  # jika ada

    predictions = []
    for idx, id_process in enumerate(id_process_list):
        predictions.append({
            "id_process": id_process,
            "predicted_emotion": predicted_emotions[idx]
        })

    # Menggunakan BERT dan Lexicon untuk menyelesaikan ambiguitas
    if data_dua_emosi:
        hasil_gabungan = process_with_bert_lexicon(db, data_dua_emosi)
        gabungan_map = {
            item["id_process"]: item["predicted_emotion"]
            for item in hasil_gabungan
        }
        for pred in predictions:
            if pred["id_process"] in gabungan_map:
                pred["predicted_emotion"] = gabungan_map[pred["id_process"]]

    # Simpan hasil prediksi
    save_prediction_results(db, predictions)
    return predictions


# Save Prediction Results to DB
def save_prediction_results(db: Session, predictions: List[Dict]) -> None:
    now = datetime.now(timezone.utc)
    for pred in predictions:
        result = db.query(ProcessResult).filter(
            ProcessResult.id_process == pred["id_process"]
        ).first()
        if result:
            if pred.get("predicted_emotion"):
                result.automatic_emotion = pred["predicted_emotion"]
            result.is_processed = True
            result.processed_at = now
    db.commit()


# Update Manual Emotion
def update_manual_emotion(db: Session, id_process: int, new_label: str) -> Dict:
    result = db.query(ProcessResult).filter(ProcessResult.id_process == id_process).first()
    if not result:
        return {"success": False, "message": "Data tidak ditemukan"}
    result.data.id_label = new_label
    db.commit()
    return {"success": True, "message": "Label manual diperbarui"}


# Update Predicted Emotion
def update_predicted_emotion(db: Session, id_process: int, new_label: str) -> Dict:
    result = db.query(ProcessResult).filter(ProcessResult.id_process == id_process).first()
    if not result:
        return {"success": False, "message": "Data tidak ditemukan"}
    result.automatic_emotion = new_label
    db.commit()
    return {"success": True, "message": "Label prediksi diperbarui"}
