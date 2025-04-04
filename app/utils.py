import re
import json
import logging
import pandas as pd
from app.constants import EMOTION_LABELS

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_text(text: str) -> str:
    """
    Membersihkan teks dari karakter khusus dan mengubahnya menjadi huruf kecil.
    """
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Hapus karakter khusus
    text = re.sub(r'\s+', ' ', text).strip()  # Hapus spasi berlebih
    return text

def validate_csv_columns(df: pd.DataFrame, required_columns: list) -> bool:
    """
    Memeriksa apakah kolom yang diperlukan ada dalam DataFrame CSV.
    """
    return all(col in df.columns for col in required_columns)

def save_metrics(metrics: dict, file_path: str):
    """
    Menyimpan metrik evaluasi model ke dalam file JSON.
    """
    with open(file_path, 'w') as f:
        json.dump(metrics, f, indent=4)

def load_metrics(file_path: str) -> dict:
    """
    Memuat metrik evaluasi model dari file JSON.
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def log_error(message: str):
    """
    Mencatat error ke dalam log.
    """
    logging.error(message)

def map_label_to_emotion(label: int) -> str:
    """
    Mengonversi label numerik menjadi label emosi sesuai dengan EMOTION_LABELS.
    """
    return EMOTION_LABELS.get(label, "tidak diketahui")
