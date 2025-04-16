import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from collections import defaultdict
import math

class ManualNaiveBayes:
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.classes = []
        self.vocab_size = 0
        self.class_word_counts = {}
        self.class_doc_counts = {}
        self.class_total_words = {}
        self.total_docs = 0
        self.fitted = False

    def fit(self, texts, labels):
        X = self.vectorizer.fit_transform(texts)
        self.vocab_size = len(self.vectorizer.get_feature_names_out())
        self.classes = list(set(labels))
        self.total_docs = len(texts)

        # Inisialisasi struktur data
        self.class_word_counts = {c: np.zeros(self.vocab_size) for c in self.classes}
        self.class_doc_counts = {c: 0 for c in self.classes}
        self.class_total_words = {c: 0 for c in self.classes}

        for i in range(len(texts)):
            label = labels[i]
            word_counts = X[i].toarray().flatten()
            self.class_word_counts[label] += word_counts
            self.class_total_words[label] += np.sum(word_counts)
            self.class_doc_counts[label] += 1

        self.fitted = True

    def predict(self, text):
        if not self.fitted:
            raise Exception("Model belum dilatih. Jalankan .fit() dulu.")

        x = self.vectorizer.transform([text]).toarray().flatten()
        log_probs = {}

        for c in self.classes:
            # Log prior
            log_prob = math.log(self.class_doc_counts[c] / self.total_docs)

            # Log likelihood dengan Laplace smoothing
            for idx in range(len(x)):
                if x[idx] > 0:
                    word_count = self.class_word_counts[c][idx]
                    total_words = self.class_total_words[c]
                    prob = (word_count + 1) / (total_words + self.vocab_size)
                    log_prob += x[idx] * math.log(prob)
            
            log_probs[c] = log_prob

        # Ambil kelas dengan nilai log_prob tertinggi
        return max(log_probs, key=log_probs.get)

    def predict_batch(self, texts):
        return [self.predict(text) for text in texts]
