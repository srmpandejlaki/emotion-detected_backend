from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.database.model_database import EmotionLabel, DataCollection, ProcessResult
from app.preprocessing.dataset_cleaning import DatasetPreprocessor

def get_all_preprocessing_results(db: Session):
    try:
        return db.query(ProcessResult).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching preprocessing results: {str(e)}")

def add_preprocessing_result(db: Session, id_data: int, text_preprocessing: str):
    try:
        # Tambahkan hasil ke ProcessResult
        result = ProcessResult(
            id_data=id_data,
            text_preprocessing=text_preprocessing
        )
        db.add(result)
        db.commit()
        db.refresh(result)
        return result
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding preprocessing result: {str(e)}")

def preprocessing_and_save(db: Session):
    try:
        # Ambil semua id_data yang sudah diproses
        processed_ids = db.query(ProcessResult.id_data).all()
        processed_ids = [pid[0] for pid in processed_ids]

        # Ambil data yang belum diproses
        unprocessed_data = db.query(DataCollection).filter(~DataCollection.id_data.in_(processed_ids)).all()

        if not unprocessed_data:
            return "Semua data sudah dipreprocessing."

        count = 0
        for item in unprocessed_data:
            preprocessor = DatasetPreprocessor(item.text_data)
            cleaned_text = preprocessor.process()  # Pastikan kamu punya method `process()`
            add_preprocessing_result(db, id_data=item.id_data, text_preprocessing=cleaned_text)

        return f"Berhasil memproses {count} data."

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing and saving preprocessing data: {str(e)}")

def get_preprocess_result_by_id(db: Session, process_id: int):
    try:
        return db.query(ProcessResult).filter(ProcessResult.id_process == process_id).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting preprocessing result by ID: {str(e)}")

def delete_preprocess_result(db: Session, process_id: int):
    try:
        process = get_preprocess_result_by_id(db, process_id)
        if not process:
            raise HTTPException(status_code=404, detail="Process Result not found")
        db.delete(process)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting preprocessing result: {str(e)}")


def delete_all_preprocess_result(db: Session):
    try:
        # Kosongkan ProcessResult
        db.query(ProcessResult).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting all preprocessing results: {str(e)}")

def update_label(db: Session, id_data: int, new_label: str):
    try:
        data = db.query(DataCollection).filter(DataCollection.id_data == id_data).first()
        if not data:
            raise HTTPException(status_code=404, detail="Data tidak ditemukan")
        
        data.label = new_label
        db.commit()
        db.refresh(data)
        return {"message": "Label berhasil diperbarui", "data": {
            "id_data": data.id_data,
            "text_data": data.text_data,
            "label": data.id_label
        }}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating label: {str(e)}")

def add_emotion_label(db: Session, emotion_name: str):
    try:
        # Cek apakah label emosi sudah ada
        existing_label = db.query(EmotionLabel).filter(EmotionLabel.emotion_name == emotion_name).first()
        if existing_label:
            raise HTTPException(status_code=400, detail="Label emosi sudah ada.")

        # Tambah label baru
        new_label = EmotionLabel(emotion_name=emotion_name)
        db.add(new_label)
        db.commit()
        db.refresh(new_label)

        return {
            "message": "Label emosi berhasil ditambahkan.",
            "data": {
                "id_label": new_label.id_label,
                "emotion_name": new_label.emotion_name
            }
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Gagal menambahkan label emosi: {str(e)}")

