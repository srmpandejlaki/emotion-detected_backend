import numpy as np
import pandas as pd
from src.processing.algorithms.naive_bayes import EmotionNaiveBayes
from src.processing.algorithms.bert_lexicon import BERTLexicon
from src.utilities.kamus_data.emotion_lexicon import SENTIMENT_LEXICON, EMOTION_LEXICON


class EmotionHybridModel:
    """
    Model Hybrid untuk Klasifikasi Emosi
    Output terbatas pada: joy, trust, shock, netral, fear, sadness, anger
    """

    def __init__(self, nb_threshold=0.7):
        self.nb_model = EmotionNaiveBayes()
        self.bert_lex = None
        self.threshold = nb_threshold
        self.label_encoder = None
        self.valid_emotions = ["joy", "trust", "shock",
                               "netral", "fear", "sadness", "anger"]

    def fit(self, X_text, y, label_encoder):
        """Train model dengan teks dan label"""
        self.label_encoder = label_encoder
        self.bert_lex = BERTLexicon(SENTIMENT_LEXICON)
        self.nb_model.fit(X_text, y, self.label_encoder)

    def _validate_emotion(self, emotion):
        """Pastikan emosi termasuk dalam 7 kategori valid"""
        return emotion if emotion in self.valid_emotions else "netral"

    def _get_emotion_from_lexicon(self, text):
        """Deteksi emosi berdasarkan kata kunci dalam lexicon"""
        words = text.lower().split()
        emotion_counts = {e: 0 for e in self.valid_emotions}

        for word in words:
            if word in EMOTION_LEXICON:
                emotion = EMOTION_LEXICON[word]
                if emotion in emotion_counts:
                    emotion_counts[emotion] += 1

        max_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0]
        return self._validate_emotion(max_emotion) if sum(emotion_counts.values()) > 0 else None

    def _map_sentiment_to_emotion(self, sentiment, text):
        """Map hasil BERT-Lexicon ke 7 emosi valid dengan konteks lebih baik"""
        bert_details = self.bert_lex.get_prediction_details(text)
        related_words = bert_details['kata_terkait']

        # Jika ada kata terkait, pertimbangkan emosi dari kata tersebut
        if related_words:
            word_emotions = [EMOTION_LEXICON.get(
                word.lower(), None) for word in related_words]
            word_emotions = [
                e for e in word_emotions if e in self.valid_emotions]

            if word_emotions:
                # Ambil emosi yang paling sering muncul di kata terkait
                from collections import Counter
                most_common = Counter(word_emotions).most_common(1)
                if most_common[0][1] > 1:  # Minimal 2 kata mendukung
                    return most_common[0][0]

        # Default mapping berdasarkan sentiment
        if sentiment == 1:  # Positif
            return 'joy' if 'joy' in self.valid_emotions else 'trust'
        else:  # Negatif
            # Bedakan antara sadness, fear, dan anger berdasarkan kata kunci
            negative_words = set(text.lower().split()) & set(
                EMOTION_LEXICON.keys())
            negative_emotions = [EMOTION_LEXICON[word] for word in negative_words
                                 if EMOTION_LEXICON[word] in ['sadness', 'fear', 'anger']]

            if negative_emotions:
                return max(set(negative_emotions), key=negative_emotions.count)
            return 'sadness'

    def get_bert_lexicon_details(self, texts, nb_predictions):
        """Return detail prediksi BERT-Lexicon"""
        details = []
        for i, text in enumerate(texts):
            bert_detail = self.bert_lex.get_prediction_details(text)
            mapped_emotion = self._map_sentiment_to_emotion(
                bert_detail['sentiment'], text)

            details.append({
                'kalimat': text,
                'prediksi_nb': nb_predictions[i],
                'prediksi_bert': mapped_emotion,
                'bobot_bert': bert_detail['bobot_bert'],
                'bobot_lexicon': bert_detail['bobot_lexicon'],
                'kata_terkait': ', '.join(bert_detail['kata_terkait'])
            })

        return details

    def predict(self, X_text):
        """Prediksi emosi dengan output terbatas 7 kategori"""
        nb_probas = self.nb_model.predict_proba(X_text)
        nb_preds = [self._validate_emotion(e)
                    for e in self.nb_model.predict(X_text)]

        y_pred = []
        pred_sources = []

        for i, text in enumerate(X_text):
            max_prob = np.max(nb_probas[i])

            if max_prob >= self.threshold:
                y_pred.append(nb_preds[i])
                pred_sources.append("Naive Bayes")
            else:
                lex_emotion = self._get_emotion_from_lexicon(text)
                if lex_emotion:
                    y_pred.append(lex_emotion)
                    pred_sources.append("Lexicon")
                else:
                    sentiment = self.bert_lex.predict_sentiment(text)
                    mapped_emotion = self._map_sentiment_to_emotion(
                        sentiment, text)
                    y_pred.append(mapped_emotion)
                    pred_sources.append("BERT-Lexicon")

        return np.array(y_pred), pred_sources
