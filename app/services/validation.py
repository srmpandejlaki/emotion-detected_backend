from sqlalchemy.orm import Session
from app import models

def classify_text(db: Session, input_text: str):
    # Dummy model (harus diganti dengan model yang sudah dilatih)
    emotions = ["senang", "percaya", "terkejut", "netral", "takut", "sedih", "marah"]
    predicted_label = 1  # Misalnya, default prediksi "senang"

    # Simpan hasil klasifikasi sebagai data latih baru
    new_data = models.Dataset(text=input_text, label=predicted_label)
    db.add(new_data)
    db.commit()

    return emotions[predicted_label - 1]

def get_results(db: Session):
    return db.query(models.ValidationResults).all()
