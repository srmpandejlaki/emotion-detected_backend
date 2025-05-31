from flask import Blueprint
from src.api.controllers.predict_controller import PredictController

predict_bp = Blueprint("predict", __name__)
predict_controller = PredictController()

# Endpoint untuk prediksi satuan
predict_bp.route("/predict", methods=["POST"])(predict_controller.predict)

# Endpoint untuk prediksi batch
predict_bp.route("/predict/batch", methods=["POST"])(predict_controller.predict_batch)
