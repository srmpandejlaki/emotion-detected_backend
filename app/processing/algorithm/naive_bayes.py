from typing import List, Dict
from app.core.utils import preprocess_text
from app.processing.alternatif_method.bert_lexicon import process_with_bert_lexicon
from app.database.model_database import ProcessResult
from app.database.schemas import PredictionResult
from sqlalchemy.orm import Session
import math
from collections import defaultdict
import datetime

# Simulasi perhitungan Naive Bayes manual (contoh sederhana)
def classify_text_naive_bayes(db: Session, texts: List[str], labels: List[str], id_process_list: List[int]) -> List[Dict]:
    # Hitung prior probabilities
    label_counts = defaultdict(int)
    total_data = len(labels)
    for label in labels:
        label_counts[label] += 1

    prior_probs = {label: count / total_data for label, count in label_counts.items()}

    # Hitung likelihood (dengan asumsi sederhana: setiap kata muncul di label tertentu)
    word_counts = defaultdict(lambda: defaultdict(int))
    for i, text in enumerate(texts):
        words = text.split()
        label = labels[i]
        for word in words:
            word_counts[label][word] += 1

    # Total kata per label
    total_words_per_label = {label: sum(word_counts[label].values()) for label in label_counts}

    predictions = []
    for idx, text in enumerate(texts):
        words = text.split()
        probs = {}

        for label in label_counts:
            log_prob = math.log(prior_probs[label])
            for word in words:
                word_freq = word_counts[label].get(word, 0) + 1  # Laplace smoothing
                word_prob = word_freq / (total_words_per_label[label] + len(word_counts[label]))
                log_prob += math.log(word_prob)
            probs[label] = log_prob

        max_prob = max(probs.values())
        predicted_labels = [label for label, p in probs.items() if p == max_prob]
        predicted_emotion = predicted_labels[0] if len(predicted_labels) == 1 else None

        predictions.append({
            "id_process": id_process_list[idx],
            "text": text,
            "probabilities": probs,
            "predicted_emotion": predicted_emotion,
        })

    # Simpan hasil prediksi
    save_prediction_results(db, predictions)

    # Cek apakah ada data ambigu dan proses ke metode gabungan
    lanjutkan_processing(db, predictions)

    return predictions


def save_prediction_results(db: Session, predictions: List[Dict]):
    now = datetime.datetime.utcnow()
    for pred in predictions:
        result = db.query(ProcessResult).filter(ProcessResult.id_process == pred["id_process"]).first()
        if result:
            if pred["predicted_emotion"]:
                result.automatic_emotion = pred["predicted_emotion"]
            result.is_processed = True
            result.processed_at = now
    db.commit()


def lanjutkan_processing(db: Session, predictions: List[Dict]):
    data_dua_emosi = []
    for pred in predictions:
        probs = pred["probabilities"]
        max_prob = max(probs.values())
        emosi_max = [e for e, p in probs.items() if p == max_prob]
        if len(emosi_max) == 2:
            data_dua_emosi.append({
                "id_process": pred["id_process"],
                "text": pred["text"]
            })

    if data_dua_emosi:
        print(f"{len(data_dua_emosi)} data masuk ke metode gabungan BERT + Lexicon...")
        process_with_bert_lexicon(db, data_dua_emosi)
