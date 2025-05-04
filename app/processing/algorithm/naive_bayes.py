import pandas as pd
import time
from typing import List, Dict, Union, Tuple
from collections import defaultdict
import math

EPSILON = 1e-10

class NaiveBayesClassifier:
    def __init__(self):
        # Atribut untuk menyimpan statistik pelatihan
        self.prior_probs = {}
        self.word_counts = defaultdict(lambda: defaultdict(int))
        self.total_words_per_label = {}
        self.vocabulary = set()
        self.vocab_size = 0

    def calculate_label_statistics(
        self, texts: List[str], labels: List[str]
    ) -> Tuple[Dict[str, float], Dict[str, Dict[str, int]], Dict[str, int]]:
        label_counts = defaultdict(int)
        word_counts = defaultdict(lambda: defaultdict(int))

        # Menghitung frekuensi label dan kata untuk setiap label
        for text, label in zip(texts, labels):
            label_counts[label] += 1
            for word in text.split():
                word_counts[label][word] += 1

        # Total kata per label dan prior probabilities
        total_words_per_label = {label: sum(words.values()) for label, words in word_counts.items()}
        prior_probs = {label: count / len(labels) for label, count in label_counts.items()}

        return prior_probs, word_counts, total_words_per_label

    def laplace_smoothing(self, count: int, total: int, vocab_size: int) -> float:
        return (count + 1) / (total + vocab_size)

    def calculate_log_probabilities(
        self, text: str
    ) -> Dict[str, float]:
        words = text.split()
        log_probs = {}

        # Menghitung log-probabilitas untuk setiap label
        for label, prior in self.prior_probs.items():
            log_prob = math.log(prior + EPSILON)
            total_words = self.total_words_per_label[label]

            for word in words:
                word_count = self.word_counts[label].get(word, 0)
                word_prob = self.laplace_smoothing(word_count, total_words, self.vocab_size)
                log_prob += math.log(word_prob + EPSILON)

            log_probs[label] = log_prob

        return log_probs

    def train(self, texts: List[str], labels: List[str]):
        # Melatih model dengan menghitung statistik label dan kata
        self.prior_probs, self.word_counts, self.total_words_per_label = self.calculate_label_statistics(texts, labels)
        self.vocabulary = {word for label in self.word_counts for word in self.word_counts[label]}
        self.vocab_size = len(self.vocabulary)

    def predict(self, texts: List[str]) -> List[str]:
        predictions = []
        for text in texts:
            log_probs = self.calculate_log_probabilities(text)
            max_log_prob = max(log_probs.values())
            predicted_labels = sorted([label for label, lp in log_probs.items() if math.isclose(lp, max_log_prob, abs_tol=1e-5)])
            predicted_emotion = predicted_labels[0] if len(predicted_labels) == 1 else None
            predictions.append(predicted_emotion)
        return predictions

    def get_ambiguous_predictions(self, texts: List[str], labels: List[str], id_process_list: List[int]):
        predictions = []
        data_dua_emosi = []
        benar = 0

        # Melakukan prediksi dengan mengidentifikasi data dengan dua emosi yang memiliki probabilitas sama
        for idx, text in enumerate(texts):
            log_probs = self.calculate_log_probabilities(text)
            max_log_prob = max(log_probs.values())
            predicted_labels = sorted([label for label, lp in log_probs.items() if math.isclose(lp, max_log_prob, abs_tol=1e-5)])
            predicted_emotion = predicted_labels[0] if len(predicted_labels) == 1 else None

            if predicted_emotion == labels[idx]:
                benar += 1

            if len(predicted_labels) == 2:
                data_dua_emosi.append({
                    "id_process": id_process_list[idx],
                    "text": text
                })

            predictions.append({
                "id_process": id_process_list[idx],
                "text": text,
                "manual_emotion": labels[idx],
                "probabilities": log_probs,
                "predicted_emotion": predicted_emotion,
            })

        akurasi = benar / len(texts) if texts else 0

        return predictions, data_dua_emosi, akurasi


if __name__ == "__main__":
    # Mulai waktu
    start_time = time.time()

    # Baca file dataset hasil preprocessing
    dataset_path = "./data/preprocessing_results/new_dataset.csv"
    df = pd.read_csv(dataset_path)

    # Validasi kolom wajib
    if not {"id_process", "text", "emotion", "preprocessed_result"}.issubset(df.columns):
        raise ValueError("CSV harus memiliki kolom: id_process, text, emotion, dan preprocessed_result")

    texts = df["preprocessed_result"].astype(str).tolist()
    labels = df["emotion"].astype(str).tolist()
    id_process_list = df["id_process"].astype(int).tolist()

    # Instansiasi NaiveBayesClassifier dan latih model
    model = NaiveBayesClassifier()
    model.train(texts, labels)

    # Jalankan prediksi
    predictions, data_dua_emosi, akurasi = model.get_ambiguous_predictions(
        texts=texts,
        labels=labels,
        id_process_list=id_process_list
    )

    # Hitung akurasi
    total_data = len(predictions)
    benar = sum(1 for p in predictions if p["predicted_emotion"] == p["manual_emotion"])
    akurasi = benar / total_data if total_data > 0 else 0

    # Tampilkan hasil
    for result in predictions:
        print("\n--- Hasil ---")
        print(f"ID        : {result['id_process']}")
        print(f"Teks      : {result['text']}")
        print(f"Manual    : {result['manual_emotion']}")
        print(f"Prediksi  : {result['predicted_emotion']}")
        print("Probabilitas log:")
        for label, prob in result["probabilities"].items():
            print(f"  {label}: {prob:.4f}")

    # Tampilkan data dengan 2 emosi setara
    print("\n--- Data dengan dua emosi probabilitas setara ---")
    for data in data_dua_emosi:
        print(f"ID: {data['id_process']} | Teks: {data['text']}")

    # Total waktu proses
    end_time = time.time()
    print(f"\nTotal waktu pelatihan dan prediksi: {end_time - start_time:.2f} detik")
    print(f"Akurasi: {akurasi * 100:.2f}%")
