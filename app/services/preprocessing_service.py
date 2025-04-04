from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Dataset
from app.utils.text_processing import preprocess_text
from app.utils.logging_utils import log_error

def process_preprocessing(db: Session):
    try:
        # Ambil dataset yang belum diberi label
        dataset = db.query(Dataset).filter(Dataset.label == None).all()

        if not dataset:
            raise HTTPException(status_code=404, detail="No data to preprocess")

        processed_data = []
        
        for data in dataset:
            processed_text = preprocess_text(data.text)
            processed_data.append({"text": processed_text, "label": data.label})
        
        return processed_data

    except Exception as e:
        log_error(f"Error in process_preprocessing: {str(e)}")
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
        log_error(f"Error in save_preprocessed_data: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
