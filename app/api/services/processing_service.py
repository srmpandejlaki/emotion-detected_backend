from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List, Dict, Tuple
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score

from app.database.model_database import ProcessResult
from app.processing.algorithm.naive_bayes import naive_bayes_classification
from app.processing.alternatif_method.bert_lexicon import process_with_bert_lexicon


def get_all_processing_data(db: Session) -> List[Dict]:
    return db.query(ProcessResult).all()


def get_preprocessed_data(db: Session) -> Tuple[List[str], List[str], List[int]]:
    results = db.query(ProcessResult).filter(
        ProcessResult.is_processed == False
    ).all()

    texts = [r.text_preprocessing for r in results]
    labels = [r.data.id_label for r in results]  # relasi ke label
    ids = [r.id_process for r in results]

    return texts, labels, ids


def _split_dataset(
    texts: List[str],
    labels: List[str],
    ids: List[int],
    test_size: float
) -> Tuple[List[str], List[str], List[int], List[str], List[str], List[int]]:
    """
    Membagi dataset berdasarkan test_size dari user.
    """
    return train_test_split(
        texts, labels, ids, test_size=test_size, random_state=42
    )


def split_dataset(db: Session, test_size: float) -> Dict[str, int]:
    """
    Split dataset dan kembalikan info jumlah data.
    """
    texts, labels, ids = get_preprocessed_data(db)
    if not texts:
        return {"message": "Tidak ada data tersedia untuk split."}

    X_train, X_test, y_train, y_test, id_train, id_test = _split_dataset(texts, labels, ids, test_size)

    return {
        "train_count": len(X_train),
        "test_count": len(X_test),
        "total": len(texts)
    }


def evaluate_model(db: Session, test_size: float) -> Dict:
    texts, labels, ids = get_preprocessed_data(db)
    if not texts:
        return {"message": "Tidak ada data yang tersedia untuk evaluasi."}

    X_train, X_test, y_train, y_test, id_train, id_test = _split_dataset(texts, labels, ids, test_size)

    # Gabungkan untuk simulasi pelatihan + prediksi uji
    predictions, _ = naive_bayes_classification(
        texts=X_train + X_test,
        labels=y_train + y_test,
        id_process_list=id_train + id_test
    )

    predicted = [
        pred["predicted_emotion"]
        for pred in predictions
        if pred["id_process"] in id_test
    ]
    actual = y_test

    all_labels = sorted(set(labels))
    cm = confusion_matrix(actual, predicted, labels=all_labels)
    precision = precision_score(actual, predicted, labels=all_labels, average=None, zero_division=0)
    recall = recall_score(actual, predicted, labels=all_labels, average=None, zero_division=0)
    accuracy = accuracy_score(actual, predicted)

    return {
        "confusion_matrix": cm.tolist(),
        "accuracy": round(accuracy, 4),
        "precision": {label: round(p, 4) for label, p in zip(all_labels, precision)},
        "recall": {label: round(r, 4) for label, r in zip(all_labels, recall)},
        "labels": all_labels
    }


def process_and_save_predictions_naive_bayes(
    db: Session,
    texts: List[str],
    labels: List[str],
    id_process_list: List[int]
) -> List[Dict]:
    predictions, data_dua_emosi = naive_bayes_classification(
        texts, labels, id_process_list
    )

    if data_dua_emosi:
        hasil_gabungan = process_with_bert_lexicon(db, data_dua_emosi)
        gabungan_map = {
            item["id_process"]: item["predicted_emotion"]
            for item in hasil_gabungan
        }
        for pred in predictions:
            if pred["id_process"] in gabungan_map:
                pred["predicted_emotion"] = gabungan_map[pred["id_process"]]

    save_prediction_results(db, predictions)
    return predictions


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


def update_manual_emotion(db: Session, id_process: int, new_label: str) -> Dict:
    result = db.query(ProcessResult).filter(ProcessResult.id_process == id_process).first()
    if not result:
        return {"success": False, "message": "Data tidak ditemukan"}
    result.data.id_label = new_label
    db.commit()
    return {"success": True, "message": "Label manual diperbarui"}


def update_predicted_emotion(db: Session, id_process: int, new_label: str) -> Dict:
    result = db.query(ProcessResult).filter(ProcessResult.id_process == id_process).first()
    if not result:
        return {"success": False, "message": "Data tidak ditemukan"}
    result.automatic_emotion = new_label
    db.commit()
    return {"success": True, "message": "Label prediksi diperbarui"}
