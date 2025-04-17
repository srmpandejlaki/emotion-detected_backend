from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.database.model_database import DataCollection, ProcessResult
from app.preprocessing.text_cleaning import preprocess_text

def get_all_preprocessing_results(db: Session):
    try:
        return db.query(ProcessResult).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching preprocessing results: {str(e)}")

def add_preprocessing_result(db: Session, id_data: int, text_preprocessing: str):
    try:
        result = ProcessResult(
            id_data=id_data,
            text_preprocessing=text_preprocessing
        )
        db.add(result)
        db.commit()
        db.refresh(result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding preprocessing result: {str(e)}")

def process_and_save_preprocessing(db: Session):
    try:
        """
        Fungsi untuk memproses data yang belum dipreprocessing.
        """
        # Ambil semua data yang belum dipreprocessing
        data = db.query(ProcessResult).filter(ProcessResult.text_preprocessing == None).all()

        if not data:
            return "Semua data sudah dipreprocessing."

        for item in data:
            # Ambil teks dari tabel DataCollection menggunakan foreign key (id_data)
            data_collection = db.query(DataCollection).filter(DataCollection.id_data == item.id_data).first()

            if data_collection:
                # Proses teks jika ada data
                cleaned = preprocess_text(data_collection.text_data)  # Gunakan fungsi preprocess_text
                item.text_preprocessing = cleaned

        db.commit()
        return f"Berhasil memproses {len(data)} data."

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing and saving preprocessing data: {str(e)}")
