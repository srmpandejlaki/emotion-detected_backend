# src/api/routes/dataset_routes.py
from flask import Blueprint
from src.api.controllers.dataset_controller import DatasetController

dataset_bp = Blueprint("dataset", __name__, url_prefix="/dataset")
dataset_controller = DatasetController()

# Route untuk mengunggah dataset

# Route untuk mengambil dataset tertentu dengan paginasi
dataset_bp.route(
    "/", methods=["GET"])(dataset_controller.get_dataset)

dataset_bp.route("/upload", methods=["POST"]
                 )(dataset_controller.upload_dataset)

# Route untuk menambah data pada dataset
dataset_bp.route("/data", methods=["POST"]
                 )(dataset_controller.add_data)

# Route untuk menghapus data dari dataset
dataset_bp.route("/data", methods=["DELETE"]
                 )(dataset_controller.delete_data)
