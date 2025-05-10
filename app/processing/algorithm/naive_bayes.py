import math
from collections import defaultdict
from typing import List, Tuple, Dict, Any


class NaiveBayesClassifier:
    def __init__(self):
        self.class_probs = {}
        self.word_probs = {}
        self.vocab = set()
        self.classes = set()
        self.total_words_per_class = defaultdict(int)
        self.word_counts_per_class = defaultdict(lambda: defaultdict(int))

    def train(self, texts: List[str], labels: List[str]):
        class_counts = defaultdict(int)
        total_texts = len(texts)

        for text, label in zip(texts, labels):
            class_counts[label] += 1
            words = text.split()
            self.total_words_per_class[label] += len(words)
            for word in words:
                self.word_counts_per_class[label][word] += 1
                self.vocab.add(word)

        self.classes = set(class_counts.keys())

        # Hitung probabilitas kelas
        self.class_probs = {
            label: math.log(count / total_texts)
            for label, count in class_counts.items()
        }

        # Hitung probabilitas kata (Laplace smoothing)
        self.word_probs = {}
        vocab_size = len(self.vocab)
        for label in self.classes:
            self.word_probs[label] = {}
            for word in self.vocab:
                count = self.word_counts_per_class[label][word]
                total = self.total_words_per_class[label]
                self.word_probs[label][word] = math.log(
                    (count + 1) / (total + vocab_size)
                )

    def predict(self, text: str) -> Tuple[str, Dict[str, float]]:
        words = text.split()
        log_probs = {}

        for label in self.classes:
            log_prob = self.class_probs[label]
            for word in words:
                if word in self.vocab:
                    log_prob += self.word_probs[label].get(word, 0)
            log_probs[label] = log_prob

        predicted = max(log_probs, key=log_probs.get)
        return predicted, log_probs

    def get_ambiguous_predictions(
        self, X_test: List[str], y_test: List[str], id_test: List[int]
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[str]]:
        results = []
        ambiguous_data = []
        ambiguous_ids = []

        for i, text in enumerate(X_test):
            predicted, probs = self.predict(text)

            # Cek dua emosi tertinggi apakah memiliki nilai yang sama
            sorted_probs = sorted(probs.items(), key=lambda item: item[1], reverse=True)
            if len(sorted_probs) >= 2 and sorted_probs[0][1] == sorted_probs[1][1]:
                ambiguous_data.append({
                    "id_process": id_test[i],
                    "text": text,
                    "manual_emotion": y_test[i],
                    "probabilities": probs
                })
                ambiguous_ids.append(id_test[i])

            results.append({
                "id_process": id_test[i],
                "text": text,
                "manual_emotion": y_test[i],
                "predicted_emotion": predicted,
                "probabilities": probs
            })

        return results, ambiguous_data, ambiguous_ids
