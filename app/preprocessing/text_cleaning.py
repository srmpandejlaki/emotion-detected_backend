import os
import pandas as pd
from typing import List
from app.utils.preprocess_text import preprocess_text

csv_path = "../../dataCollection/kaget.csv"

# Lokasi folder output CSV
OUTPUT_FOLDER = "preprocessing_results"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)  # Bikin folder kalau belum ada

def preprocess_single_text_from_path(file_path: str) -> str:
    """
    Membaca satu file teks, preprocessing, tampilkan di terminal, dan simpan ke CSV.
    """
    if not os.path.exists(file_path):
        print("File tidak ditemukan.")
        return ""

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        cleaned_text = preprocess_text(text)

        # Tampilkan di terminal
        print("\n=== Hasil Preprocessing (Single Text) ===")
        print(f"Original Text:\n{text}\n")
        print(f"Cleaned Text:\n{cleaned_text}\n")

        # Simpan ke CSV
        output_path = os.path.join(OUTPUT_FOLDER, "preprocessed_single_text.csv")
        df = pd.DataFrame([{"original_text": text, "cleaned_text": cleaned_text}])
        df.to_csv(output_path, index=False, encoding="utf-8")

        print(f"Hasil disimpan ke: {output_path}")

        return cleaned_text

    except Exception as e:
        raise ValueError(f"Gagal membaca atau memproses file: {e}")

def preprocess_batch_texts_from_csv(csv_path: str) -> List[dict]:
    """
    Membaca file CSV berisi banyak teks, preprocessing semua, tampilkan progress, dan simpan ke CSV.
    """
    if not os.path.exists(csv_path):
        print("File tidak ditemukan.")
        return []

    try:
        df = pd.read_csv(csv_path)

        if "text" not in df.columns:
            raise ValueError("CSV harus memiliki kolom 'text'.")

        texts = df["text"].tolist()
        cleaned_texts = []

        print("\n=== Mulai Preprocessing Batch ===")

        for idx, text in enumerate(texts, start=1):
            cleaned = preprocess_text(text)
            cleaned_texts.append(cleaned)

            # Tampilkan progress di terminal
            print(f"[{idx}/{len(texts)}] Original: {text[:30]}... --> Cleaned: {cleaned[:30]}...")

        # Simpan hasil ke CSV
        output_path = os.path.join(OUTPUT_FOLDER, "preprocessed_batch_texts.csv")
        output_df = pd.DataFrame({
            "original_text": texts,
            "cleaned_text": cleaned_texts
        })
        output_df.to_csv(output_path, index=False, encoding="utf-8")

        print(f"\nHasil batch preprocessing disimpan ke: {output_path}")

        return [
            {"original_text": orig, "cleaned_text": clean}
            for orig, clean in zip(texts, cleaned_texts)
        ]

    except Exception as e:
        raise ValueError(f"Gagal membaca atau memproses CSV: {e}")
