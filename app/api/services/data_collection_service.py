import os
import math
import shutil
import pandas as pd
from app.database import schemas
from sqlalchemy.orm import Session
from app.database import model_database
from fastapi import HTTPException, UploadFile


def get_all_data_collections(db: Session, page: int = 1, limit: int = 10):
    total_data = db.query(model_database.DataCollection).count()
    total_pages = math.ceil(total_data / limit) if limit > 0 else 1
    offset = (page - 1) * limit

    data_query = (
        db.query(model_database.DataCollection)
        .order_by(model_database.DataCollection.id_data.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total_data": total_data,
        "current_page": page,
        "total_pages": total_pages,
        "data": data_query
    }


def get_data_collection_by_id(db: Session, data_id: int):
    return db.query(model_database.DataCollection).filter(
        model_database.DataCollection.id_data == data_id
    ).first()

def create_data_collection(
    db: Session,
    data: schemas.DataCollectionCreate = None,
    file: UploadFile = None  # pakai langsung dari FastAPI
):
    if file:
        file_location = f"temp/{file.filename}"
        os.makedirs("temp", exist_ok=True)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return upload_csv_data(db, file_location)

    elif data:
        return [create_single_data(db, data)]

    else:
        raise HTTPException(status_code=400, detail="Harus mengirimkan file CSV atau data manual.")

def create_single_data(db: Session, data: schemas.DataCollectionCreate):
    db_data = model_database.DataCollection(
        text_data=data.text_data,
        id_label=data.id_label
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def upload_csv_data(db: Session, file_path: str):
    try:
        df = pd.read_csv(file_path)

        if 'text' not in df.columns or 'emotion' not in df.columns:
            raise HTTPException(status_code=400, detail="CSV harus memiliki kolom 'text' dan 'emotion'.")

        created_data = []
        for _, row in df.iterrows():
            data = schemas.DataCollectionCreate(
                text_data=row['text'],
                id_label=row['emotion'] if not pd.isnull(row['emotion']) else None
            )
            created = create_single_data(db, data)
            created_data.append(created)

        return created_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memproses file CSV: {str(e)}")

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

def delete_data_collection(db: Session, data_id: int):
    data = get_data_collection_by_id(db, data_id)
    if not data:
        raise HTTPException(status_code=404, detail="Data Collection not found")
    db.delete(data)
    db.commit()

def delete_all_data_collections(db: Session):
    db.query(model_database.DataCollection).delete()
    db.commit()
