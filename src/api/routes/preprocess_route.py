# src/api/routes/preprocess_routes.py
from flask import Blueprint
from src.api.controllers.preprocess_controller import PreprocessController

preprocess_bp = Blueprint("preprocess", __name__, url_prefix="/dataset")
preprocess_controller = PreprocessController()

# Route untuk mengambil data dengan filter
preprocess_bp.route(
    "/preprocessed/data", methods=["GET"])(preprocess_controller.get_preprocessed_data)

# Route untuk melakukan preprocessing data baru
preprocess_bp.route(
    "/preprocessed/process", methods=["POST"])(preprocess_controller.preprocess_new_data)

# Route untuk mengedit data baru
preprocess_bp.route("/preprocessed/data/<int:id>",
                    methods=["PUT"])(preprocess_controller.edit_new_data)

# Route untuk menghapus data baru
preprocess_bp.route(
    "/preprocessed/data", methods=["DELETE"])(preprocess_controller.delete_new_data)

# Route untuk menandai data sebagai sudah di-train
preprocess_bp.route(
    "/preprocessed/mark-trained", methods=["POST"])(preprocess_controller.mark_as_trained)
