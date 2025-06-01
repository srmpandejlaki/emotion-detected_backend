import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from src.features.classifier import TweetClassifier


class PredictService:

    def predict(self, text, model_path='./src/storage/models/trained/8fa43f64-ec68-42af-a5f8-3a7a8e6237a1.joblib'):
        """Mengklasifikasikan teks tunggal menggunakan model hybrid dan DeepSeek"""
        classifier = TweetClassifier(model_path)
        result = classifier.classify(text)
        return result

    def predictBatch(
        self,
        texts: list[str],
        true_labels: list[str],
        model_path='./src/storage/models/trained/8fa43f64-ec68-42af-a5f8-3a7a8e6237a1.joblib'
    ) -> dict:
        """
        Melakukan prediksi batch terhadap list teks, kemudian menghitung metrik evaluasi.
        Hasil return hanya berisi hasil prediksi dan evaluation_metrics.
        """
        if not texts or not true_labels or len(texts) != len(true_labels):
            return {"error": "Texts and labels must be provided and have the same length"}, 400

        classifier = TweetClassifier(model_path)

        predictions = []
        for text in texts:
            pred = classifier.classify(text)
            predictions.append(pred)

        # Buat list hasil prediksi lengkap
        predict_results = [
            {"text": text, "true_label": true, "predicted_emotion": pred}
            for text, true, pred in zip(texts, true_labels, predictions)
        ]

        # Hitung metrik evaluasi
        evaluation_metrics = {
            "accuracy": accuracy_score(true_labels, predictions),
            "confusion_matrix": confusion_matrix(true_labels, predictions).tolist(),
            "classification_report": classification_report(true_labels, predictions, output_dict=True)
        }

        return {
            "predict_results": predict_results,
            "evaluation_metrics": evaluation_metrics
        }

