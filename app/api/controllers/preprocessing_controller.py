from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.database.schemas import PreprocessingCreate, PreprocessingUpdate
from app.api.services import preprocessing_service
from app.database.models import DataCollection, ProcessResult
from app.preprocessing.dataset_cleaning import DatasetPreprocessor  

def run_preprocessing_by_id_controller(id_data: int, db: Session):
    try:
        return preprocessing_service.run_preprocessing_for_id(id_data, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def run_preprocessing_many_controller(db: Session, id_data_list: list[int]):
    if not id_data_list:
        raise HTTPException(status_code=400, detail="List ID kosong.")

    # Ambil semua id_data yang sudah pernah dipreprocessing
    existing_ids = db.query(ProcessResult.id_data).filter(ProcessResult.id_data.in_(id_data_list)).all()
    existing_ids_set = {id_tuple[0] for id_tuple in existing_ids}

    # Filter hanya data yang belum pernah dipreprocessing
    new_ids = [id_data for id_data in id_data_list if id_data not in existing_ids_set]

    if not new_ids:
        return {"message": "Semua data sudah dipreprocessing.", "processed_count": 0}

    # Inisialisasi DatasetPreprocessor dan akses text_preprocessor-nya
    preprocessor = DatasetPreprocessor()
    text_cleaner = preprocessor.text_preprocessor

    processed_count = 0
    for id_data in new_ids:
        data_obj = db.query(DataCollection).filter(DataCollection.id_data == id_data).first()
        if not data_obj:
            continue

        hasil = text_cleaner.preprocess(data_obj.text)  # Pakai preprocess dari TextPreprocessor
        new_result = ProcessResult(
            id_data=id_data,
            text_preprocessing=hasil,
            is_processed=True
        )
        db.add(new_result)
        processed_count += 1

    db.commit()

    return {
        "message": "Preprocessing berhasil untuk data baru.",
        "processed_count": processed_count,
        "skipped_count": len(id_data_list) - processed_count,
        "skipped_ids": list(existing_ids_set),
    }

def create_preprocessing_controller(db: Session, request: PreprocessingCreate):
    result = preprocessing_service.create_preprocessing_result(db, request)
    if not result:
        raise HTTPException(status_code=404, detail="Data tidak ditemukan.")
    return result


def get_all_preprocessing_controller(db: Session, page: int = 1, limit: int = 10):
    return preprocessing_service.get_all_preprocessing_results(db, page, limit)


def get_preprocessing_by_id_controller(db: Session, id_process: int):
    result = preprocessing_service.get_preprocessing_result_by_id(db, id_process)
    if not result:
        raise HTTPException(status_code=404, detail="Preprocessing tidak ditemukan.")
    return result


def update_preprocessing_controller(db: Session, id_process: int, update_data: PreprocessingUpdate):
    result = preprocessing_service.update_preprocessing_result(db, id_process, update_data)
    if not result:
        raise HTTPException(status_code=404, detail="Preprocessing tidak ditemukan.")
    return result


def delete_preprocessing_controller(db: Session, id_process: int):
    result = preprocessing_service.delete_preprocessing_result(db, id_process)
    if not result:
        raise HTTPException(status_code=404, detail="Preprocessing tidak ditemukan.")
    return {"message": "Preprocessing berhasil dihapus."}
