import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB


class EmotionNaiveBayes:
    """
    Naive Bayes Classifier untuk klasifikasi emosi berbasis TF-IDF.
    Menggunakan MultinomialNB dari scikit-learn.
    """

    def __init__(self):
        self.classes_ = None
        self.class_priors_ = None
        self.class_means_ = None
        self.class_vars_ = None
        self.tfidf_vectorizer = TfidfVectorizer(max_features=None)
        self.label_encoder = None
        self.sklearn_nb = MultinomialNB()

    def fit(self, X_text, y, label_encoder):
        """
        Melatih model Naive Bayes menggunakan MultinomialNB.
        """
        self.label_encoder = label_encoder
        self.classes_ = label_encoder.classes_

        # Transform teks ke TF-IDF
        X_tfidf = self.tfidf_vectorizer.fit_transform(X_text)
        y = np.array(y)

        # Train model scikit-learn
        self.sklearn_nb.fit(X_tfidf, y)

        # Simpan parameter yang diperlukan
        self.class_priors_ = self.sklearn_nb.class_count_ / \
            self.sklearn_nb.class_count_.sum()
        self.class_means_ = np.exp(self.sklearn_nb.feature_log_prob_)
        # MultinomialNB tidak memiliki varian
        self.class_vars_ = np.zeros_like(self.class_means_)

    def get_prior_probabilities(self, X_text):
        """
        Mengembalikan DataFrame probabilitas prior setiap kelas.
        """
        if self.class_priors_ is None:
            raise ValueError(
                "Model belum di-fit. Panggil fit() terlebih dahulu.")

        total_samples = int(self.sklearn_nb.class_count_.sum())

        data = []
        for class_index, label in enumerate(self.classes_):
            data.append({
                'label': label,
                'frekuensi': int(self.sklearn_nb.class_count_[class_index]),
                'probabilitas': self.class_priors_[class_index]
            })

        return data

    def get_word_probabilities(self):
        """
        Mengembalikan DataFrame probabilitas kata per label.
        """
        if self.class_means_ is None:
            raise ValueError(
                "Model belum di-fit. Panggil fit() terlebih dahulu.")

        vocab = self.tfidf_vectorizer.get_feature_names_out()
        data = []

        for class_index, label in enumerate(self.classes_):
            for word_index, word in enumerate(vocab):
                data.append({
                    'kata': word,
                    'label': label,
                    'probabilitas': self.class_means_[class_index, word_index]
                })

        return data

    def get_tfidf_details(self, texts):
        """
        Mengembalikan detail TF, IDF, dan TF-IDF untuk setiap kata dalam teks.
        """
        if not hasattr(self.tfidf_vectorizer, 'vocabulary_'):
            raise ValueError(
                "TF-IDF vectorizer belum di-fit. Panggil fit() terlebih dahulu.")

        count_vectorizer = CountVectorizer(
            vocabulary=self.tfidf_vectorizer.vocabulary_)
        count_matrix = count_vectorizer.transform(texts)
        tfidf_matrix = self.tfidf_vectorizer.transform(texts)

        vocab = self.tfidf_vectorizer.get_feature_names_out()
        idf_values = self.tfidf_vectorizer.idf_

        details = []
        for i, text in enumerate(texts):
            tfidf_row = tfidf_matrix[i]
            count_row = count_matrix[i]
            indices = tfidf_row.nonzero()[1]

            for j in indices:
                details.append({
                    'kalimat': text,
                    'kata': vocab[j],
                    'tf': count_row[0, j],
                    'idf': idf_values[j],
                    'tfidf': tfidf_row[0, j]
                })

        return details

    def predict(self, X_text):
        """
        Mengembalikan prediksi label untuk input teks.
        """
        if self.classes_ is None:
            raise ValueError(
                "Model belum di-fit. Panggil fit() terlebih dahulu.")

        X_tfidf = self.tfidf_vectorizer.transform(X_text)
        predictions = self.sklearn_nb.predict(X_tfidf)
        return np.array([self.classes_[i] for i in predictions])

    def predict_proba(self, X_text):
        """
        Mengembalikan probabilitas prediksi untuk input teks.
        """
        if self.classes_ is None:
            raise ValueError(
                "Model belum di-fit. Panggil fit() terlebih dahulu.")

        X_tfidf = self.tfidf_vectorizer.transform(X_text)
        return self.sklearn_nb.predict_proba(X_tfidf)
