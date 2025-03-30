from sqlalchemy.orm import Session
from app import models

def save_to_db(db: Session, data: list[dict]):
    for row in data:
        new_data = models.Dataset(text=row["text"], label=row["label"])
        db.add(new_data)
    db.commit()
