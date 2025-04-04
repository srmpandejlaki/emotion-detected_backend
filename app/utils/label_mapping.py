from app.constants import EMOTION_LABELS

def map_label_to_emotion(label: int) -> str:
    """
    Mengonversi label numerik menjadi label emosi sesuai dengan EMOTION_LABELS.
    """
    return EMOTION_LABELS.get(label, "tidak diketahui")
