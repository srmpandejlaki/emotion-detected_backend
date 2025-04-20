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

def preprocessing_and_save(db: Session):
    try:
        """
        Fungsi untuk memproses data yang belum dipreprocessing.
        Hanya memproses data dari DataCollection yang belum ada di ProcessResult.
        """
        # Ambil semua id_data yang sudah ada di ProcessResult
        processed_ids = db.query(ProcessResult.id_data).all()
        processed_ids = [pid[0] for pid in processed_ids]  # hasil query berupa list of tuple

        # Ambil semua data dari DataCollection yang belum diproses
        unprocessed_data = db.query(DataCollection).filter(~DataCollection.id_data.in_(processed_ids)).all()

        if not unprocessed_data:
            return "Semua data sudah dipreprocessing."

        count = 0
        for item in unprocessed_data:
            cleaned = preprocess_text(item.text_data)
            add_preprocessing_result(db, id_data=item.id_data, text_preprocessing=cleaned)
            count += 1

        return f"Berhasil memproses {count} data."

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing and saving preprocessing data: {str(e)}")

def get_preprocess_result_by_id(db: Session, process_id: int):
    return db.query(ProcessResult).filter(ProcessResult.id_process == process_id).first()

def delete_preprocess_result(db: Session, process_id: int):
    process = get_preprocess_result_by_id(db, process_id)
    if not process:
        raise HTTPException(status_code=404, detail="Process Result not found")
    db.delete(process)
    db.commit()

def delete_all_preprocess_result(db: Session):
    db.query(ProcessResult).delete()
    db.commit()
