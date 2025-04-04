from sqlalchemy.orm import Session
from app.models import PreprocessedData

def save_preprocessed_data(db: Session, data: list):
    """
    Menyimpan data hasil preprocessing atau klasifikasi ke database.
    :param db: Session SQLAlchemy
    :param data: List of dict, setiap dict berisi 'cleaned_text' dan 'label'
    """
    try:
        for item in data:
            cleaned_text = item["cleaned_text"]
            label = item["label"]

            # Cek apakah data sudah ada (berdasarkan cleaned_text)
            existing = db.query(PreprocessedData).filter(PreprocessedData.cleaned_text == cleaned_text).first()
            if existing:
                existing.label = label  # Update label jika sudah ada
            else:
                new_data = PreprocessedData(cleaned_text=cleaned_text, label=label)
                db.add(new_data)

        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Gagal menyimpan data ke database: {str(e)}")
