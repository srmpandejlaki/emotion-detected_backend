import os
import math
import shutil
import pandas as pd
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.database import schemas
from app.database.models import model_database

# Get all data collections with pagination
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


# Get single data collection by ID
def get_data_collection_by_id(db: Session, data_id: int):
    return db.query(model_database.DataCollection).filter(
        model_database.DataCollection.id_data == data_id
    ).first()


# Create single data collection (manual)
def create_single_data(db: Session, data: schemas.DataCollectionCreate):
    if not data.text_data or data.id_label is None:
        raise HTTPException(status_code=400, detail="Field 'text_data' dan 'id_label' tidak boleh kosong.")
    
    db_data = model_database.DataCollection(
        text_data=data.text_data.strip(),
        id_label=data.id_label
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

# Upload CSV
def upload_csv_data(db: Session, file_path: str):
    try:
        df = pd.read_csv(file_path)

        # Normalisasi nama kolom
        df.columns = df.columns.str.strip().str.lower()

        if 'text' not in df.columns or 'emotion' not in df.columns:
            raise HTTPException(status_code=400, detail="CSV harus memiliki kolom 'text' dan 'emotion'.")

        created_data = []

        # Ambil semua label emosi dari database dan buat dictionary {emotion_name: id_label}
        label_lookup = {label.emotion_name.lower(): label.id_label for label in db.query(model_database.EmotionLabel).all()}

        for _, row in df.iterrows():
            if pd.isna(row['text']):
                continue  # skip baris kosong

            emotion_name = str(row['emotion']).strip().lower() if not pd.isna(row['emotion']) else None
            id_label = label_lookup.get(emotion_name) if emotion_name else None

            data = schemas.DataCollectionCreate(
                text_data=str(row['text']).strip(),
                id_label=id_label
            )

            created = create_single_data(db, data)
            created_data.append(created)

        return created_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memproses file CSV: {str(e)}")

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

# Entry point for creating (manual or file)
def create_data_collection(
    db: Session,
    data: schemas.DataCollectionCreate = None,
    file: UploadFile = None
):
    if file:
        os.makedirs("temp", exist_ok=True)
        file_location = f"temp/{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return upload_csv_data(db, file_location)

    elif data:
        return [create_single_data(db, data)]

    else:
        raise HTTPException(status_code=400, detail="Harus mengirimkan file CSV atau data manual.")


# Delete by ID
def delete_data_collection(db: Session, data_id: int):
    data = get_data_collection_by_id(db, data_id)
    if not data:
        raise HTTPException(status_code=404, detail="Data Collection tidak ditemukan")
    db.delete(data)
    db.commit()


# Delete all
def delete_all_data_collections(db: Session):
    db.query(model_database.DataCollection).delete()
    db.commit()
