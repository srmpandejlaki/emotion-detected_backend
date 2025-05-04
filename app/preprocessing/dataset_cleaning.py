import pandas as pd
import csv
import os

from app.preprocessing.preprocessor import Preprocessor
from app.preprocessing.text_cleaning import TextPreprocessor


class DatasetPreprocessor(Preprocessor):
    def __init__(self):
        self.text_preprocessor = TextPreprocessor()

    def read_file(self, file_path):
        """Deteksi dan baca file, baik CSV atau Excel"""
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".csv":
            return pd.read_csv(file_path, encoding="utf-8")
        elif ext in [".xls", ".xlsx"]:
            return pd.read_excel(file_path, engine="openpyxl")
        else:
            raise ValueError("Format file tidak didukung: harus .csv, .xls, atau .xlsx")

    def process(self, df):
        """Proses teks menjadi bentuk preprocessed"""
        if "text" not in df.columns:
            raise ValueError("Kolom 'text' harus ada")

        df["preprocessed_result"] = df["text"].apply(
            self.text_preprocessor.preprocess
        )
        df.drop_duplicates(subset=["preprocessed_result"], inplace=True)
        df.dropna(subset=["preprocessed_result"], inplace=True)

        return df

    def raw_formatter(self, file_path):
        """Baca file (Excel atau CSV), proses, dan simpan hasil akhir"""
        try:
            df = self.read_file(file_path)

            if "text" not in df.columns:
                raise ValueError("Kolom 'text' harus ada di file")

            df['text'] = df['text'].astype(str).str.replace('"', "'")

            df_processed = self.process(df)

            os.makedirs("./data/preprocessing_results", exist_ok=True)
            final_path = "./data/preprocessing_results/new_dataset.csv"
            df_processed.to_csv(final_path, index=False,
                                quoting=csv.QUOTE_NONNUMERIC, encoding="utf-8")

            print(f"Hasil preprocessing berhasil disimpan ke: {final_path}")

        except Exception as e:
            print(f"Terjadi kesalahan: {e}")


if __name__ == "__main__":
    preprocessor = DatasetPreprocessor()
    preprocessor.raw_formatter("./data/dataCollection/komentar.xlsx")
