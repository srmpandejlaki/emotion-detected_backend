from typing import List, Dict, Union, Tuple
from collections import defaultdict
import math, time

EPSILON = 1e-10

def calculate_label_statistics(
    texts: List[str], 
    labels: List[str]
) -> Tuple[Dict[str, float], Dict[str, Dict[str, int]], Dict[str, int]]:
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
        log_prob = math.log(prior + EPSILON)
        total_words = total_words_per_label[label]

        for word in words:
            word_count = word_counts[label].get(word, 0)
            word_prob = laplace_smoothing(word_count, total_words, vocab_size)
            log_prob += math.log(word_prob + EPSILON)

        log_probs[label] = log_prob

    return log_probs


def naive_bayes_classification(
    texts: List[str],
    labels: List[str],
    id_process_list: List[int]
) -> Tuple[
    List[Dict[str, Union[int, str, None, Dict[str, float]]]],
    List[Dict[str, Union[int, str]]]
]:
    if not (len(texts) == len(labels) == len(id_process_list)):
        raise ValueError("Panjang texts, labels, dan id_process_list harus sama")

    prior_probs, word_counts, total_words_per_label = calculate_label_statistics(texts, labels)
    vocabulary = {word for label in word_counts for word in word_counts[label]}
    vocab_size = len(vocabulary)

    predictions = []
    data_dua_emosi = []

    for idx, text in enumerate(texts):
        log_probs = calculate_log_probabilities(
            text, prior_probs, word_counts, total_words_per_label, vocab_size
        )

        max_log_prob = max(log_probs.values())
        predicted_labels = sorted([
            label for label, lp in log_probs.items() 
            if math.isclose(lp, max_log_prob, abs_tol=1e-5)
        ])

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

    return predictions, data_dua_emosi

if __name__ == "__main__":
    import pandas as pd

    # Mulai waktu
    start_time = time.time()

    # Baca file dataset hasil preprocessing
    dataset_path = "./preprocessing_results/new_dataset.csv"
    df = pd.read_csv(dataset_path)

    # Validasi kolom wajib
    if not {"id_process", "text", "emotion", "preprocessed_result"}.issubset(df.columns):
        raise ValueError("CSV harus memiliki kolom: text, emotion, dan preprocessed_result")

    texts = df["preprocessed_result"].astype(str).tolist()
    labels = df["emotion"].astype(str).tolist()
    id_process_list = df["id_process"].astype(int).tolist()

    # Dummy session karena tidak pakai DB saat ini
    # dummy_db: Session = MagicMock()

    # Jalankan training dan klasifikasi
    predictions, data_dua_emosi = naive_bayes_classification(
        texts=texts,
        labels=labels,
        id_process_list=id_process_list
    )

    # Tampilkan hasil
    for result in predictions:
        print("\n--- Hasil ---")
        print(f"ID        : {result['id_process']}")
        print(f"Teks      : {result['text']}")
        print(f"Manual      : {result['emotion']}")
        print(f"Prediksi  : {result['predicted_emotion']}")
        print("Probabilitas log:")
        for label, prob in result["probabilities"].items():
            print(f"  {label}: {prob:.4f}")
        print("\n--- Data dengan dua emosi probabilitas setara ---")
    for data in data_dua_emosi:
        print(f"ID: {data['id_process']} | Teks: {data['text']}")


    # Total waktu proses
    end_time = time.time()
    print(f"\nTotal waktu pelatihan dan prediksi: {end_time - start_time:.2f} detik")
