import numpy as np
import re
from collections import defaultdict


class BERTLexicon:
    """
    Versi ringan dari BERT-Lexicon.
    Menggunakan perhitungan manual dan lexicon match berbasis skor.
    """

    def __init__(self, lexicon_dict):
        self.lexicon = lexicon_dict
        self.valid_emotions = ["joy", "trust", "shock",
                               "netral", "fear", "sadness", "anger"]

    def _tokenize(self, text):
        return re.findall(r'\b\w+\b', text.lower())

    def get_prediction_details(self, text):
        tokens = self._tokenize(text)
        related_words = []
        sentiment_scores = []
        emotion_counts = defaultdict(int)
        total_score = 0
        total_weight = 0

        for word in tokens:
            if word in self.lexicon:
                score = self.lexicon[word]
                sentiment_scores.append(score)
                related_words.append(word)
                total_score += abs(score)
                total_weight += 1

                # Jika juga ada di EMOTION_LEXICON, hitung juga
                from src.utilities.kamus_data.emotion_lexicon import EMOTION_LEXICON
                emo = EMOTION_LEXICON.get(word)
                if emo in self.valid_emotions:
                    emotion_counts[emo] += 1

        if total_weight > 0:
            avg_sentiment = np.mean(sentiment_scores)
            sentiment = 1 if avg_sentiment > 0 else 0
            avg_weight = total_score / total_weight
        else:
            sentiment = 0
            avg_weight = 0
            avg_sentiment = 0

        return {
            'sentiment': sentiment,
            # sebenarnya bukan BERT tapi tetap pakai nama untuk konsistensi
            'bobot_bert': avg_weight,
            'bobot_lexicon': avg_sentiment,
            'kata_terkait': related_words,
            'similaritas': np.array([1.0] * len(related_words)),
            'skor_sentimen': np.array(sentiment_scores)
        }

    def predict_sentiment(self, text):
        details = self.get_prediction_details(text)
        return details['sentiment']
