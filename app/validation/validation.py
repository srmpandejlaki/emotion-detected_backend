from typing import List, Dict, Union
from sqlalchemy.orm import Session
from app.utils.evaluation_model import evaluate_model
from app.processing.algorithm.naive_bayes import (
    calculate_label_statistics,
    calculate_log_probabilities
)
import math

EPSILON = 1e-10


def validate_model_on_test_data(
    db: Session,
    test_texts: List[str],
    test_labels: List[str],
    train_texts: List[str],
    train_labels: List[str]
) -> Dict[str, Union[List, Dict]]:

    # Hitung statistik dari data latih
    prior_probs, word_counts, total_words_per_label = calculate_label_statistics(train_texts, train_labels)
    vocabulary = {word for label in word_counts for word in word_counts[label]}
    vocab_size = len(vocabulary)

    # Prediksi data uji
    predictions = []
    for text in test_texts:
        log_probs = calculate_log_probabilities(text, prior_probs, word_counts, total_words_per_label, vocab_size)
        max_log_prob = max(log_probs.values())
        predicted_labels = [label for label, lp in log_probs.items() if math.isclose(lp, max_log_prob, abs_tol=1e-5)]
        predicted_emotion = predicted_labels[0] if len(predicted_labels) == 1 else predicted_labels[0]

        predictions.append(predicted_emotion)

    # Evaluasi model
    evaluation = evaluate_model(test_labels, predictions)

    return {
        "test_texts": test_texts,
        "true_labels": test_labels,
        "predicted_labels": predictions,
        "evaluation": evaluation
    }
