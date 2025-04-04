import joblib
from app.utils.logging_utils import log_error

def save_model(model, vectorizer, path: str):
    """
    Menyimpan model dan vectorizer ke dalam file .pkl.
    """
    try:
        joblib.dump((model, vectorizer), path)
    except Exception as e:
        log_error(f"Gagal menyimpan model ke {path}: {str(e)}")

def load_model(path: str):
    """
    Memuat model dan vectorizer dari file .pkl.
    """
    try:
        return joblib.load(path)
    except Exception as e:
        log_error(f"Gagal memuat model dari {path}: {str(e)}")
        return None, None
