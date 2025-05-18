# src/api/controllers/preprocess_controller.py
import os
from flask import request, jsonify
from sqlalchemy.orm import Session
from src.api.services.preprocess_service import PreprocessService
from src.api.services.dataset_service import DatasetService
from src.api.services.process_service import ProcessService


class PreprocessController:
    preprocess_service = PreprocessService()
    dataset_service = DatasetService()
    process_service = ProcessService()

    def __init__(self):
        pass

    def preprocess_new_data(self):
        """Melakukan preprocessing pada data baru"""
        result, status_code = self.preprocess_service.preprocess_new_data()
        return jsonify(result), status_code

    def get_preprocessed_data(self):
        """Mengambil data preprocessed dengan filter"""
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        filter_type = request.args.get('filter', 'all')

        result = self.preprocess_service.fetch_preprocessed_data(
            page, limit, filter_type)
        if "error" in result:
            return jsonify(result), 404
        return jsonify(result), 200

    def edit_new_data(self, id):
        """Mengedit data baru"""
        data = request.json
        new_emotion = data.get("new_emotion")
        new_text = data.get("new_text")

        result, status_code = self.preprocess_service.edit_new_data(
            id, new_emotion, new_text)
        return jsonify(result), status_code

    def delete_new_data(self):
        """Menghapus data baru"""
        data = request.json
        if not isinstance(data, list):
            return jsonify({"error": "Expected an array of indices"}), 400

        result, status_code = self.preprocess_service.delete_new_data(data)
        return jsonify(result), status_code

    def mark_as_trained(self):
        """Menandai data sebagai sudah di-train"""
        data = request.json
        if not isinstance(data, list):
            return jsonify({"error": "Expected an array of ids"}), 400

        result, status_code = self.preprocess_service.mark_data_as_trained(
            data)
        return jsonify(result), status_code
