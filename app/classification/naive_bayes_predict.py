import csv
from collections import defaultdict
import math
from typing import List, Tuple

def train_naive_bayes(data: List[Tuple[str, str]]):
    label_counts = defaultdict(int)
    word_counts = defaultdict(lambda: defaultdict(int))
    vocabulary = set()

    for text, label in data:
        words = text.split()
        label_counts[label] += 1
        for word in words:
            word_counts[label][word] += 1
            vocabulary.add(word)

    return label_counts, word_counts, vocabulary

def predict_naive_bayes(text: str, label_counts, word_counts, vocabulary):
    total_docs = sum(label_counts.values())
    vocab_size = len(vocabulary)
    scores = {}
    input_words = text.split()

    for label in label_counts:
        log_prob = math.log(label_counts[label] / total_docs)
        total_words_in_label = sum(word_counts[label].values())

        for word in input_words:
            word_freq = word_counts[label].get(word, 0)
            prob_word_given_label = (word_freq + 1) / (total_words_in_label + vocab_size)
            log_prob += math.log(prob_word_given_label)

        scores[label] = log_prob

    return max(scores, key=scores.get)

if __name__ == "__main__":
    csv_file = "./preprocessing_results/new_dataset.csv"
    data = []

    # Baca CSV
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = row["preprocessed_result"].strip()
            label = row["emotion"].strip()
            data.append((text, label))

    # Split train-test sederhana: 80% train, 20% test
    split_idx = int(0.8 * len(data))
    train_data = data[:split_idx]
    test_data = data[split_idx:]

    # Train
    label_counts, word_counts, vocabulary = train_naive_bayes(train_data)

    # Uji dan tampilkan hasil prediksi
    correct = 0
    print("\nHasil Prediksi Naive Bayes:")
    for text, actual_label in test_data:
        predicted = predict_naive_bayes(text, label_counts, word_counts, vocabulary)
        is_correct = predicted == actual_label
        if is_correct:
            correct += 1
        print(f"Teks: '{text}'")
        print(f"Label Asli: {actual_label} | Prediksi: {predicted} | {'✅ Benar' if is_correct else '❌ Salah'}\n")

    accuracy = correct / len(test_data) * 100 if test_data else 0
    print(f"Akurasi: {accuracy:.2f}%")
