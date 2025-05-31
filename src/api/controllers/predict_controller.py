from flask import request, jsonify
from src.api.services.predict_service import PredictService
import os


class PredictController:
    predict_service = PredictService()

    def __init__(self):
        pass

    def predict(self):
        """ Menerima input teks dan mengembalikan hasil prediksi """
        try:
            data = request.json
            if not data or "text" not in data:
                return jsonify({"error": "Text is required"}), 400

            text = data["text"]

            result = self.predict_service.predict(text)
            return jsonify(result), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def predict_batch(self):
        """ Menerima daftar teks dan label, lalu mengembalikan hasil prediksi dan evaluasi """
        try:
            data = request.json
            if not data:
                return jsonify({"error": "Request body is required"}), 400

            texts = data.get("texts")
            true_labels = data.get("true_labels")

            if not texts or not true_labels:
                return jsonify({"error": "Both 'texts' and 'true_labels' are required"}), 400

            if len(texts) != len(true_labels):
                return jsonify({"error": "Length of 'texts' and 'true_labels' must be the same"}), 400

            result = self.predict_service.predictBatch(texts, true_labels)
            if isinstance(result, tuple):  # handle (result_dict, 400) case
                return jsonify(result[0]), result[1]

            return jsonify(result), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
