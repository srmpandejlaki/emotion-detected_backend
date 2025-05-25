# src/api/services/dataset_service.py
from datetime import datetime
from sqlalchemy import func
from src.database.config import SessionLocal
from src.database.models import Dataset, PreprocessedDataset
from src.preprocessing.extends.dataset_preprocessor import DatasetPreprocessor
from src.api.services.preprocess_service import PreprocessService


class DatasetService:
    """Layanan untuk mengelola dataset"""
    db = SessionLocal()
    preprocessor = DatasetPreprocessor()
    preprocess_service = PreprocessService()
    DATASET_DIR = "./src/storage/datasets/uploaded"

    def __init__(self):
        pass

    def save_dataset(self, filepath):
        """Melakukan preprocessing, menyimpan dataset, dan mencatat metadata"""
        processed_df = self.preprocessor.preprocess(filepath, sep=",")
        if processed_df.empty:
            return {"error": "Dataset is empty after preprocessing"}, 400

        # Save the dataset to the database
        for _, row in processed_df.iterrows():
            dataset = Dataset(
                text=row['text'],
                emotion=row['emotion'],
                inserted_at=datetime.utcnow()
            )
            self.db.add(dataset)
            self.db.flush()
            preprocessed = PreprocessedDataset(
                dataset_id=dataset.id,
                text=row['text'],
                emotion=row['emotion'],
                is_preprocessed=False,
                is_trained=False,
                inserted_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            self.db.add(preprocessed)
        self.db.commit()
        return {"message": "Dataset saved successfully"}, 201

    def fetch_dataset(self, page=1, limit=10):
        """Mengambil dataset tertentu dengan paginasi"""
        offset = (page - 1) * limit
        total = self.db.query(Dataset).count()
        datasets = self.db.query(Dataset).offset(offset).limit(limit).all()
        # label counts mengembalikan jumlah data per label dalam bentuk dictionary
        label_counts = self.db.query(Dataset.emotion, func.count(Dataset.id)).group_by(
            Dataset.emotion).all()
        label_counts = {emotion: count for emotion, count in label_counts}

        datasets = [
            {
                "id": dataset.id,
                "text": dataset.text,
                "emotion": dataset.emotion,
                "inserted_at": dataset.inserted_at
            } for dataset in datasets
        ]

        return {
            "data": datasets,
            "total_pages": (total + limit - 1) // limit,
            "current_page": page,
            "limit": limit,
            "total_data": total,
            "label_counts": label_counts,
        }

    def add_data(self, data_list):
        """Menambahkan data baru ke dataset"""
        new_records = []
        for data in data_list:
            dataset = Dataset(
                text=data['text'],
                emotion=data['emotion'],
                inserted_at=datetime.utcnow()
            )
            self.db.add(dataset)
            self.db.flush()  # To get the ID

            preprocessed = PreprocessedDataset(
                dataset_id=dataset.id,
                text=data['text'],
                emotion=data['emotion'],
                is_preprocessed=False,
                is_trained=False,
                inserted_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            self.db.add(preprocessed)
            new_records.append(preprocessed)

        self.db.commit()
        return {"message": f"Added {len(new_records)} new records"}, 201

    def delete_data(self, indexes):
        """Menghapus data dari dataset"""
        # Delete from both tables
        deleted_count = 0
        for idx in indexes:
            dataset = self.db.query(Dataset).get(idx)
            if dataset:
                self.db.query(PreprocessedDataset).filter_by(
                    dataset_id=idx).delete()
                self.db.delete(dataset)
                deleted_count += 1

        self.db.commit()
        return {"message": f"Removed {deleted_count} records"}, 200
