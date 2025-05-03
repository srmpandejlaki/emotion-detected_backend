from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List, Dict, Tuple
from app.database.model_database import ProcessResult
from app.processing.algorithm.naive_bayes import naive_bayes_classification
from app.processing.alternatif_method.bert_lexicon import process_with_bert_lexicon

def get_preprocessed_data(db: Session) -> Tuple[List[str], List[str], List[int]]:
    results = db.query(ProcessResult).filter(
        ProcessResult.is_processed == False
    ).all()

    texts = [r.text_preprocessing for r in results]
    labels = [r.data.emotion.emotion_name for r in results]  # Ambil dari relasi berantai
    ids = [r.id_process for r in results]

    return texts, labels, ids


def save_prediction_results(
    db: Session, 
    predictions: List[Dict]
) -> None:
    """
    Simpan hasil prediksi ke database berdasarkan id_process.
    """
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


def process_and_save_predictions_naive_bayes(
    db: Session,
    texts: List[str],
    labels: List[str],
    id_process_list: List[int]
) -> List[Dict]:
    """
    Proses klasifikasi menggunakan Naive Bayes dan simpan hasilnya.
    Bila terdapat dua emosi dengan skor yang sama, lanjutkan ke metode BERT + Lexicon.
    """
    # Proses klasifikasi Naive Bayes
    predictions, data_dua_emosi = naive_bayes_classification(
        texts, labels, id_process_list
    )

    # Tangani data ambigu (2 emosi sama kuat) dengan metode gabungan
    if data_dua_emosi:
        hasil_gabungan = process_with_bert_lexicon(db, data_dua_emosi)
        gabungan_map = {
            item["id_process"]: item["predicted_emotion"]
            for item in hasil_gabungan
        }
        for pred in predictions:
            if pred["id_process"] in gabungan_map:
                pred["predicted_emotion"] = gabungan_map[pred["id_process"]]

    # Simpan ke database
    save_prediction_results(db, predictions)

    return predictions
