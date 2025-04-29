from typing import List, Dict, Union
from app.processing.alternatif_method.bert_lexicon import process_with_bert_lexicon
from app.database.model_database import ProcessResult
from sqlalchemy.orm import Session
from collections import defaultdict
import math
import datetime

EPSILON = 1e-10  # Untuk menghindari log(0)

def calculate_label_statistics(
    texts: List[str], 
    labels: List[str]
) -> tuple[Dict[str, float], Dict[str, Dict[str, int]], Dict[str, int]]:
    label_counts = defaultdict(int)
    word_counts = defaultdict(lambda: defaultdict(int))

    for text, label in zip(texts, labels):
        label_counts[label] += 1
        for word in text.split():
            word_counts[label][word] += 1

    total_words_per_label = {label: sum(words.values()) for label, words in word_counts.items()}
    prior_probs = {label: count / len(labels) for label, count in label_counts.items()}

    return prior_probs, word_counts, total_words_per_label


def laplace_smoothing(
    count: int, total: int, vocab_size: int
) -> float:
    return (count + 1) / (total + vocab_size)


def calculate_log_probabilities(
    text: str,
    prior_probs: Dict[str, float],
    word_counts: Dict[str, Dict[str, int]],
    total_words_per_label: Dict[str, int],
    vocab_size: int
) -> Dict[str, float]:
    words = text.split()
    log_probs = {}

    for label, prior in prior_probs.items():
        log_prob = math.log(prior + EPSILON)  # Hindari log(0)
        total_words = total_words_per_label[label]

        for word in words:
            word_count = word_counts[label].get(word, 0)
            word_prob = laplace_smoothing(word_count, total_words, vocab_size)
            log_prob += math.log(word_prob + EPSILON)

        log_probs[label] = log_prob

    return log_probs


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
        log_probs = calculate_log_probabilities(text, prior_probs, word_counts, total_words_per_label, vocab_size)

        max_log_prob = max(log_probs.values())
        predicted_labels = [label for label, lp in log_probs.items() if math.isclose(lp, max_log_prob, abs_tol=1e-5)]

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

    if data_dua_emosi:
        print(f"{len(data_dua_emosi)} data masuk ke metode gabungan BERT + Lexicon...")
        hasil_gabungan = process_with_bert_lexicon(db, data_dua_emosi)
        
        # Update hasil prediksi
        gabungan_map = {item["id_process"]: item["predicted_emotion"] for item in hasil_gabungan}
        for pred in predictions:
            if pred["id_process"] in gabungan_map:
                pred["predicted_emotion"] = gabungan_map[pred["id_process"]]

    save_prediction_results(db, predictions)

    return predictions


def save_prediction_results(
    db: Session, 
    predictions: List[Dict[str, Union[str, int, None, Dict[str, float]]]]
):
    now = datetime.datetime.utcnow()
    for pred in predictions:
        result = db.query(ProcessResult).filter(ProcessResult.id_process == pred["id_process"]).first()
        if result:
            if pred["predicted_emotion"]:
                result.automatic_emotion = pred["predicted_emotion"]
            result.is_processed = True
            result.processed_at = now
    db.commit()
