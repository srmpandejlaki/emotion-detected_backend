# src/api/controllers/dataset_controller.py
import os
import pandas as pd
from flask import request, jsonify
from src.api.services.dataset_service import DatasetService
from src.api.services.preprocess_service import PreprocessService
from src.api.services.process_service import ProcessService


class DatasetController:

    dataset_service = DatasetService()
    preprocess_service = PreprocessService()
    process_service = ProcessService()

    def __init__(self):
        pass

    def upload_dataset(self):
        """Mengunggah dataset, menyimpannya, dan menjalankan preprocessing"""
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        if not file.filename.lower().endswith('.csv'):
            return jsonify({"error": "Only CSV files are allowed"}), 400

        filepath = os.path.join(
            self.dataset_service.DATASET_DIR, file.filename)
        file.save(filepath)

        try:
            df = pd.read_csv(filepath, sep=',')
        except pd.errors.EmptyDataError:
            return jsonify({"error": "Uploaded Dataset file is empty or has no parsable columns"}), 400

        required_columns = {"emotion", "text"}
        if not required_columns.issubset(df.columns):
            return jsonify({"error": "Dataset must contain 'emotion' and 'text' columns"}), 400

        if df.empty:
            return jsonify({"error": "Dataset has no data"}), 400

        allowed_topics = {"joy", "trust",
                          "shock", "netral", "fear", "sadness", "anger"}
        actual_topics = set(df["emotion"].unique())
        invalid_topics = actual_topics - allowed_topics
        if invalid_topics:
            return jsonify({"error": f"Invalid topics found: {', '.join(invalid_topics)}"}), 400

        dataset_info = self.dataset_service.save_dataset(
            filepath)

        return jsonify({
            "message": "Dataset uploaded successfully",
            "dataset": dataset_info,
        }), 200

    def get_dataset(self):
        """Mengambil dataset tertentu dengan paginasi"""
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))

        result = self.dataset_service.fetch_dataset(page, limit)
        if result is None:
            return jsonify({"error": "Dataset not found"}), 404

        return jsonify(result), 200

    def add_data(self):
        """Menambahkan data baru ke dataset"""

        data = request.json
        if not isinstance(data, list):
            return jsonify({"error": "Expected an array of data"}), 400

        # Validate each item in the array
        for item in data:
            if "text" not in item or "emotion" not in item:
                return jsonify({"error": "Each item must contain 'emotion' and 'text'"}), 400

        result, status_code = self.dataset_service.add_data(data)
        return jsonify(result), status_code

    def delete_data(self):
        """Menghapus data dari dataset"""

        data = request.json
        if not isinstance(data, list):
            return jsonify({"error": "Expected an array of content indexes"}), 400

        result, status_code = self.dataset_service.delete_data(
            data)
        return jsonify(result), status_code
