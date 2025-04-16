import nltk
from sqlalchemy.orm import Session
from app.database.model_database import Dataset
from fastapi import HTTPException

nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def process_preprocessing(db: Session):
    try:
        # Ambil dataset yang perlu diproses
        dataset = db.query(Dataset).filter(Dataset.label == None).all()

        if not dataset:
            raise HTTPException(status_code=404, detail="No data to preprocess")

        processed_data = []
        
        for data in dataset:
            text = data.text
            # Tokenisasi dan hapus stopwords
            words = word_tokenize(text)
            words = [word for word in words if word.isalnum()]  # Hapus tanda baca
            stop_words = set(stopwords.words("indonesian"))
            words = [word for word in words if word not in stop_words]
            
            # Lematisasi atau stemming (jika diperlukan)
            # Anda bisa menggunakan Lemmatizer atau Stemmer dari NLTK atau Spacy
            
            processed_text = " ".join(words)
            processed_data.append({"text": processed_text, "label": data.label})
        
        return processed_data

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def save_preprocessed_data(data: list, db: Session):
    try:
        for item in data:
            # Update label setelah preprocessing
            existing_data = db.query(Dataset).filter(Dataset.text == item["text"]).first()
            if existing_data:
                existing_data.text = item["text"]
                existing_data.label = item["label"]
            else:
                # Jika data belum ada, tambahkan sebagai data baru
                new_data = Dataset(text=item["text"], label=item["label"])
                db.add(new_data)
        
        db.commit()
        return {"message": "Data successfully saved"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))