# src/api/services/preprocess_service.py
from datetime import datetime
from src.database.config import SessionLocal
from sqlalchemy import func
from src.database.models import PreprocessedDataset
from src.preprocessing.extends.text_preprocessor import TextPreprocessor
import string


class PreprocessService:
    """Layanan untuk mengelola preprocessing data"""
    db = SessionLocal()
    text_preprocessor = TextPreprocessor()

    def __init__(self):
        pass

    def preprocess_new_data(self):
        """Melakukan preprocessing pada data baru yang belum diproses"""
        unprocessed = self.db.query(PreprocessedDataset).filter_by(
            is_preprocessed=False).all()

        if not unprocessed:
            return {"error": "No new data to preprocess"}, 400

        unique_contents = {}
        duplicate_count = 0

        for record in unprocessed:
            preprocessed_content = self.text_preprocessor.preprocess(
                record.text)

            if not preprocessed_content:
                continue

            # Check for duplicates
            exists = self.db.query(PreprocessedDataset).filter(
                PreprocessedDataset.preprocessed_text == preprocessed_content,
                PreprocessedDataset.is_preprocessed == True
            ).first()

            if exists or preprocessed_content in unique_contents.values():
                duplicate_count += 1
                self.db.delete(record)
            else:
                unique_contents[record.id] = preprocessed_content
                record.preprocessed_text = preprocessed_content
                record.is_preprocessed = True
                record.updated_at = datetime.utcnow()

        self.db.commit()

        if not unique_contents:
            return {
                "error": "No unique data after preprocessing",
                "details": {
                    "total_processed": len(unprocessed),
                    "duplicates_found": duplicate_count,
                    "unique_added": 0
                }
            }, 400

        return {
            "message": f"Preprocessed {len(unique_contents)} new unique records",
            "results": {
                "total_processed": len(unprocessed),
                "duplicates_found": duplicate_count,
                "unique_added": len(unique_contents),
                "sample_unique_content": list(unique_contents.values())[:3] if unique_contents else []
            }
        }, 200

    def add_new_data(self, data_list):
        """Menambahkan data baru ke dataset"""
        new_records = []
        duplicate_count = 0

        for data in data_list:
            # Check for existing content
            exists = self.db.query(PreprocessedDataset).filter(
                PreprocessedDataset.text == data['text']
            ).first()

            if exists:
                duplicate_count += 1
                continue

            new_record = PreprocessedDataset(
                text=data['text'],
                emotion=data['label'],
                is_preprocessed=False,
                is_trained=False,
                inserted_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            new_records.append(new_record)

        if not new_records:
            return {"error": "All data already exists"}, 409

        self.db.bulk_save_objects(new_records)
        self.db.commit()

        return {
            "message": f"Added {len(new_records)} new records ({duplicate_count} duplicates skipped)",
            "added_count": len(new_records),
            "duplicate_count": duplicate_count
        }, 201

    def fetch_preprocessed_data(self, page=1, limit=10, filter_type="all"):
        """Mengambil data dengan filter dan paginasi"""
        query = self.db.query(PreprocessedDataset)

        # Apply filters
        if filter_type == "old":
            query = query.filter(PreprocessedDataset.is_trained == True)
        elif filter_type == "new":
            query = query.filter(PreprocessedDataset.is_trained == False)
        elif filter_type == "unprocessed":
            query = query.filter(PreprocessedDataset.is_preprocessed == False)
        elif filter_type == "processed":
            query = query.filter(PreprocessedDataset.is_preprocessed == True)

        # Get total counts for stats
        total_all = self.db.query(PreprocessedDataset).count()
        total_old = self.db.query(PreprocessedDataset).filter(
            PreprocessedDataset.is_trained == True).count()
        total_new = self.db.query(PreprocessedDataset).filter(
            PreprocessedDataset.is_trained == False).count()
        total_preprocessed = self.db.query(PreprocessedDataset).filter(
            PreprocessedDataset.is_preprocessed == True).count()
        total_unprocessed = self.db.query(PreprocessedDataset).filter(
            PreprocessedDataset.is_preprocessed == False).count()

        # Get topic counts
        topic_counts_all = dict(self.db.query(
            PreprocessedDataset.emotion,
            func.count(PreprocessedDataset.emotion)
        ).group_by(PreprocessedDataset.emotion).all())

        # Apply pagination
        total_data = query.count()
        data = query.offset((page - 1) * limit).limit(limit).all()

        return {
            "data": [{
                "id": d.id,
                "text": d.text,
                "preprocessed_text": d.preprocessed_text,
                "emotion": d.emotion,
                "is_preprocessed": d.is_preprocessed,
                "is_trained": d.is_trained,
                "inserted_at": d.inserted_at.isoformat() if d.inserted_at else None,
                "updated_at": d.updated_at.isoformat() if d.updated_at else None
            } for d in data],
            "total_data": total_data,
            "total_pages": (total_data + limit - 1) // limit,
            "current_page": page,
            "limit": limit,
            "topic_counts": dict(self.db.query(
                PreprocessedDataset.emotion,
                func.count(PreprocessedDataset.emotion)
            ).group_by(PreprocessedDataset.emotion).all()),
            "stats": {
                "total_all": total_all,
                "total_old": total_old,
                "total_new": total_new,
                "total_preprocessed": total_preprocessed,
                "total_unprocessed": total_unprocessed,
                "topic_counts_all": topic_counts_all
            }
        }

    def edit_new_data(self, record_id, new_label=None, new_content=None):
        """Mengedit data baru (yang belum di-train)"""
        record = self.db.query(PreprocessedDataset).get(record_id)
        if not record:
            return {"error": "Data not found"}, 404

        # Hanya bisa edit data yang belum di-train
        if record.is_trained:
            return {"error": "Cannot edit trained data"}, 403

        # Validasi content
        if new_content:
            if len(new_content) == 1:
                return {"error": "Data must be at least 2 characters"}, 400

            for word in new_content.split():
                if word.isdigit():
                    return {"error": f"Data cannot contain word with only number: '{word}'"}, 400
                elif word in string.punctuation:
                    return {"error": f"Data cannot contain word with only punctuation character: '{word}'"}, 400
                elif all(char in string.punctuation for char in word):
                    return {"error": f"Data cannot contain word with only punctuation characters: '{word}'"}, 400

            # Check for duplicate content
            exists = self.db.query(PreprocessedDataset).filter(
                PreprocessedDataset.preprocessed_text == new_content,
                PreprocessedDataset.id != record_id
            ).first()
            if exists:
                return {"error": "Data already exists in the dataset"}, 400

        # Apply changes
        if new_label:
            record.emotion = new_label
        if new_content:
            record.preprocessed_text = new_content

        record.updated_at = datetime.utcnow()
        self.db.commit()

        return {"message": "Data updated successfully"}, 200

    def delete_new_data(self, record_ids):
        """Menghapus data baru (yang belum di-train)"""
        # Filter hanya data yang belum di-train
        to_delete = self.db.query(PreprocessedDataset).filter(
            PreprocessedDataset.id.in_(record_ids),
            PreprocessedDataset.is_trained == False
        ).all()

        if not to_delete:
            return {"error": "No deletable data found (only new/un-trained data can be deleted)"}, 404

        deleted_count = 0
        for record in to_delete:
            self.db.delete(record)
            deleted_count += 1

        self.db.commit()
        return {"message": f"Deleted {deleted_count} records"}, 200

    def mark_data_as_trained(self, record_ids):
        """Menandai data sebagai sudah di-train"""
        # Pastikan data sudah diproses
        unprocessed = self.db.query(PreprocessedDataset).filter(
            PreprocessedDataset.id.in_(record_ids),
            PreprocessedDataset.is_preprocessed == False
        ).count()

        if unprocessed > 0:
            return {"error": f"{unprocessed} data are not preprocessed yet"}, 400

        # Update records
        self.db.query(PreprocessedDataset).filter(
            PreprocessedDataset.id.in_(record_ids)
        ).update({
            "is_trained": True,
            "updated_at": datetime.utcnow()
        }, synchronize_session=False)

        self.db.commit()
        return {"message": f"Marked {len(record_ids)} records as trained"}, 200
