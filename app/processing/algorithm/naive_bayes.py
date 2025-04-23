from typing import List, Dict, Union
from app.processing.alternatif_method.bert_lexicon import process_with_bert_lexicon
from app.database.model_database import ProcessResult
from sqlalchemy.orm import Session
import math
from collections import defaultdict
import datetime


def calculate_label_statistics(texts: List[str], labels: List[str]):
    label_counts = defaultdict(int)
    word_counts = defaultdict(lambda: defaultdict(int))

    for text, label in zip(texts, labels):
        label_counts[label] += 1
        for word in text.split():
            word_counts[label][word] += 1

    total_words_per_label = {label: sum(words.values()) for label, words in word_counts.items()}
    prior_probs = {label: count / len(labels) for label, count in label_counts.items()}

    return prior_probs, word_counts, total_words_per_label


def laplace_smoothing(count: int, total: int, vocab_size: int) -> float:
    return (count + 1) / (total + vocab_size)


def classify_text_naive_bayes(
    db: Session,
    texts: List[str],
    labels: List[str],
    id_process_list: List[int]
) -> List[Dict[str, Union[str, int, None, Dict[str, float]]]]:

    prior_probs, word_counts, total_words_per_label = calculate_label_statistics(texts, labels)
    vocabulary = {word for label in word_counts for word in word_counts[label]}
    vocab_size = len(vocabulary)

    predictions = []
    data_dua_emosi = []

    for idx, text in enumerate(texts):
        words = text.split()
        log_probs = {}

        for label in prior_probs:
            log_prob = math.log(prior_probs[label])
            total_words = total_words_per_label[label]

            for word in words:
                word_count = word_counts[label].get(word, 0)
                word_prob = laplace_smoothing(word_count, total_words, vocab_size)
                log_prob += math.log(word_prob)

            log_probs[label] = log_prob

        max_log_prob = max(log_probs.values())
        predicted_labels = [label for label, lp in log_probs.items() if lp == max_log_prob]
        predicted_emotion = predicted_labels[0] if len(predicted_labels) == 1 else None

        if len(predicted_labels) == 2:
            data_dua_emosi.append({
                "id_process": id_process_list[idx],
                "text": text
            })

        predictions.append({
            "id_process": id_process_list[idx],
            "text": text,
            "probabilities": log_probs,
            "predicted_emotion": predicted_emotion,
        })

    # Jika ada data ambigu, proses dengan metode gabungan
    if data_dua_emosi:
        print(f"{len(data_dua_emosi)} data masuk ke metode gabungan BERT + Lexicon...")
        hasil_gabungan = process_with_bert_lexicon(db, data_dua_emosi)
        # Update hasil prediksi dengan hasil dari BERT + Lexicon
        for gabungan in hasil_gabungan:
            for pred in predictions:
                if pred["id_process"] == gabungan["id_process"]:
                    pred["predicted_emotion"] = gabungan["predicted_emotion"]

    save_prediction_results(db, predictions)

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
