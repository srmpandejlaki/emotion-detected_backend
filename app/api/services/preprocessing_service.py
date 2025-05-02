from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.database.model_database import DataCollection, ProcessResult
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
