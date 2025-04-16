import nltk
from sqlalchemy.orm import Session
from app.database.model_database import Dataset, PreprocessedData
from fastapi import HTTPException

nltk.download("stopwords")
nltk.download("punkt")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def process_preprocessing(db: Session):
    try:
        dataset = db.query(Dataset).all()

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
            new_entry = PreprocessedData(
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
