import json
from sqlalchemy.orm import Session
from app.database.config import SessionLocal
from app.database.models.model_database import EmotionLabel

def seed_emotion_labels(file_path: str):
    # Buka sesi database
    db: Session = SessionLocal()

    with open(file_path, 'r', encoding='utf-8') as file:
        labels = json.load(file)

        for item in labels:
            # Cek apakah label sudah ada
            existing = db.query(EmotionLabel).filter_by(id_label=item['id_label']).first()
            if not existing:
                label = EmotionLabel(
                    id_label=item['id_label'],
                    emotion_name=item['emotion_name']
                )
                db.add(label)

        db.commit()
        print(f"{len(labels)} labels inserted (yang belum ada).")

    db.close()

# Jalankan script jika langsung dieksekusi
if __name__ == '__main__':
    seed_emotion_labels('./app/utils/json/labels.json')
