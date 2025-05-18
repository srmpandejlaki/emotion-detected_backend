# src/api/controllers/process_controller.py
import os
from flask import request, jsonify
from src.api.services.process_service import ProcessService
from src.api.services.preprocess_service import PreprocessService


class ProcessController:
    """Controller untuk mengelola proses dataset dan model"""
    preprocess_service = PreprocessService()
    process_service = ProcessService()

    def __init__(self):
        pass

    def split_dataset(self):
        try:
            data = request.json
            if "test_size" not in data:
                return jsonify({"error": "Missing or invalid required parameters"}), 400

            test_size = data["test_size"]

            if not isinstance(test_size, (int, float)) or test_size <= 0 or test_size >= 1:
                return jsonify({"error": "Test size must be a positive float between 0 and 1"}), 400

            result = self.process_service.split_dataset(test_size)

            if "error" in result:
                return jsonify(result), 400

            allowed_labels = {"joy", "trust", "shock",
                              "netral", "fear", "sadness", "anger"}
            test_counts = result.get("test_per_label", {})

            if any(test_counts.get(label, 0) == 0 for label in allowed_labels):
                return jsonify({"error": "There is a label that is empty after splitting"}), 400

            return jsonify(result)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def train_model(self):
        try:
            data = request.json
            required_keys = ["test_size"]
            if not all(key in data for key in required_keys):
                return jsonify({"error": "Missing or invalid required parameters"}), 400

            test_size = data["test_size"]
            nb_threshold = data.get("nb_threshold", 0)

            if not isinstance(test_size, (int, float)) or test_size <= 0 or test_size >= 1:
                return jsonify({"error": "Test size must be a positive float between 0 and 1"}), 400

            stats = self.preprocess_service.fetch_preprocessed_data(
                filter_type="unprocessed")["stats"]
            if stats["total_unprocessed"] > 0:
                return jsonify({
                    "error": f"Cannot train model: {stats['total_unprocessed']} data are not preprocessed yet",
                    "unprocessed_count": stats["total_unprocessed"]
                }), 400

            result = self.process_service.train_model(test_size, nb_threshold)
            if "error" in result:
                return jsonify(result), 400

            return jsonify(result)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_models(self):
        try:
            result = self.process_service.get_models_list()
            if not result:
                return jsonify({"error": "No models found"}), 404
            return jsonify({"models": result})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_model(self, model_id):
        try:
            result = self.process_service.get_model(model_id)
            if not result:
                return jsonify({"error": "Model not found"}), 404
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_model_evaluation(self, model_id):
        try:
            result = self.process_service.get_evaluation_metrics(model_id)
            if not result:
                return jsonify({"error": "Evaluation not found"}), 404
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def fetch_prob_prior(self, model_id):
        try:
            result = self.process_service.get_prior_probabilities(model_id)
            if not result:
                return jsonify({"error": "Prior probabilities not found"}), 404
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def fetch_tfidf_stats(self, model_id):
        try:
            page = int(request.args.get("page", 1))
            limit = int(request.args.get("limit", 10))
            result = self.process_service.get_tfidf_details(model_id)
            if not result:
                return jsonify({"error": "TFIDF stats not found"}), 404

            # Manual pagination since we're loading all data
            start = (page - 1) * limit
            end = start + limit
            paginated_data = result[start:end]

            return jsonify({
                "data": paginated_data,
                "total_data": len(result),
                "total_pages": (len(result) + limit - 1) // limit,
                "current_page": page,
                "limit": limit
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def fetch_prob_condition(self, model_id):
        try:
            page = int(request.args.get("page", 1))
            limit = int(request.args.get("limit", 10))
            result = self.process_service.get_word_probabilities(model_id)
            if not result:
                return jsonify({"error": "Word probabilities not found"}), 404

            # Manual pagination
            start = (page - 1) * limit
            end = start + limit
            paginated_data = result[start:end]

            return jsonify({
                "data": paginated_data,
                "total_data": len(result),
                "total_pages": (len(result) + limit - 1) // limit,
                "current_page": page,
                "limit": limit
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def fetch_bert_lexicon(self, model_id):
        try:
            page = int(request.args.get("page", 1))
            limit = int(request.args.get("limit", 10))
            result = self.process_service.get_bert_lexicon_details(model_id)
            if not result:
                return jsonify({"error": "BERT lexicon details not found"}), 404

            # Manual pagination
            start = (page - 1) * limit
            end = start + limit
            paginated_data = result[start:end]

            return jsonify({
                "data": paginated_data,
                "total_data": len(result),
                "total_pages": (len(result) + limit - 1) // limit,
                "current_page": page,
                "limit": limit
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def fetch_predict_results(self, model_id):
        try:
            page = int(request.args.get("page", 1))
            limit = int(request.args.get("limit", 10))

            result = self.process_service.get_predict_results(
                model_id, page, limit)
            if not result:
                return jsonify({"error": "Predict results not found"}), 404

            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
