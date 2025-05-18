from flask import Blueprint
from src.api.controllers.process_controller import ProcessController

process_bp = Blueprint("process", __name__)
process_controller = ProcessController()

process_bp.route("/process/split",
                 methods=["POST"])(process_controller.split_dataset)
process_bp.route("/process/train",
                 methods=["POST"])(process_controller.train_model)
process_bp.route("/process/models/",
                 methods=["GET"])(process_controller.get_models)
process_bp.route("/process/model/<model_id>",
                 methods=["GET"])(process_controller.get_model)

# Endpoint metadata tambahan & CSV pagination
process_bp.route("/process/model/evaluation/<model_id>",
                 methods=["GET"])(process_controller.get_model_evaluation)
process_bp.route("/process/model/tfidf-stats/<model_id>",
                 methods=["GET"])(process_controller.fetch_tfidf_stats)
process_bp.route("/process/model/fetch-prob-prior/<model_id>",
                 methods=["GET"])(process_controller.fetch_prob_prior)
process_bp.route("/process/model/fetch-prob-condition/<model_id>",
                 methods=["GET"])(process_controller.fetch_prob_condition)
process_bp.route("/process/model/fetch-bert-lexicon/<model_id>",
                 methods=["GET"])(process_controller.fetch_bert_lexicon)
process_bp.route("/process/model/predict-results/<model_id>",
                 methods=["GET"])(process_controller.fetch_predict_results)
