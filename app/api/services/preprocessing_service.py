import nltk
from sqlalchemy.orm import Session
from app.database.model_database import DataCollection, ProcessResult
from fastapi import HTTPException
from app.database.model_database import ProcessResult

nltk.download("stopwords")
nltk.download("punkt")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def process_preprocessing(db: Session):
    try:
        dataset = db.query(DataCollection).all()

        if not dataset:
            raise HTTPException(status_code=404, detail="No data found")

        stop_words = set(stopwords.words("indonesian"))
        processed_data = []

        for data in dataset:
            words = word_tokenize(data.text)
            words = [word for word in words if word.isalnum() and word.lower() not in stop_words]
            cleaned_text = " ".join(words)

            processed_data.append({
                "original_id": data.id,
                "original_text": data.text,
                "cleaned_text": cleaned_text,
                "label": data.label
            })

        return processed_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def save_preprocessed_data(processed_data: list, db: Session):
    try:
        for item in processed_data:
            # Simpan ke tabel hasil preprocessing
            new_entry = ProcessResult(
                original_id=item["original_id"],
                original_text=item["original_text"],
                cleaned_text=item["cleaned_text"],
                label=item["label"]
            )
            db.add(new_entry)
        
        db.commit()
        return {"message": "Preprocessed data saved successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_all_preprocessing_results(db: Session):
    return db.query(ProcessResult).all()

def add_preprocessing_result(db: Session, id_data: int, text_preprocessing: str):
    result = ProcessResult(
        id_data=id_data,
        text_preprocessing=text_preprocessing
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result
