import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
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

    def predict(self, text, use_fallback=False):
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

        # Deteksi apakah ada dua kelas dengan log_prob yang sama
        sorted_probs = sorted(log_probs.items(), key=lambda item: item[1], reverse=True)
        top_class = sorted_probs[0][0]
        second_class = sorted_probs[1][0] if len(sorted_probs) > 1 else None

        # Jika dua kelas memiliki probabilitas yang sama, gunakan fallback
        if sorted_probs[0][1] == sorted_probs[1][1] and use_fallback:
            # Panggil fungsi fallback yang menggabungkan BERT + Lexicon
            fallback_class = self.fallback(text, top_class, second_class)
            return fallback_class

        return top_class

    def predict_batch(self, texts, use_fallback=False):
        return [self.predict(text, use_fallback) for text in texts]

    def fallback(self, text, class_1, class_2):
        # Fallback logic: combine BERT and Lexicon to resolve conflict
        # Misalnya, BERT akan melakukan prediksi untuk kedua kelas dan Lexicon memberi bobot lebih
        # Bergantung pada implementasi BERT dan Lexicon kamu, di sini misalnya kita panggil fungsi external
        # Contoh implementasi fallback ini, pastikan menggunakan metode sesuai dengan logika yang ada.

        # Contoh logika fallback yang menggunakan BERT dan Lexicon
        # Ini hanya placeholder, implementasi aktual harus disesuaikan
        from app.processing.fallback.bert_lexicon_fallback import combined_score  # Mengimpor fungsi fallback
        
        final_prediction = combined_score(text, class_1, class_2)
        return final_prediction
