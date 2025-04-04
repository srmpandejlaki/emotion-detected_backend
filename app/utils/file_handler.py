import json
import pandas as pd

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
