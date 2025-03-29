from sqlalchemy.orm import Session
from app.utils.database import SessionLocal
from app.models.label_emosi import LabelEmosi

def seed_labels():
    db: Session = SessionLocal()

    emosi_list = [
        (1, "senang"),
        (2, "percaya"),
        (3, "terkejut"),
        (4, "netral"),
        (5, "takut"),
        (6, "sedih"),
        (7, "marah"),
    ]

    for id_emosi, nama in emosi_list:
        if not db.query(LabelEmosi).filter_by(id=id_emosi).first():
            db.add(LabelEmosi(id=id_emosi, nama_emosi=nama))
    
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_labels()
