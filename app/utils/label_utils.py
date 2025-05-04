from sqlalchemy.orm import Session
from app.database.models.model_database import EmotionLabel

def get_label_id_map(db: Session) -> dict:
    """
    Mengambil mapping nama_emotion ke id_label dari database.
    
    Returns:
        Dict[str, int]: Mapping nama_emotion -> id_label
    """
    labels = db.query(EmotionLabel).all()
    return {label.emotion_name: label.id_label for label in labels}
