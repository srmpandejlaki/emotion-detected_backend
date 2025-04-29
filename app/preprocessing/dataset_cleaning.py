import pandas as pd
import csv
from app.preprocessing.preprocessor import Preprocessor
from app.preprocessing.text_cleaning import TextPreprocessor


class DatasetPreprocessor(Preprocessor):
    def __init__(self):
        self.text_preprocessor = TextPreprocessor()

    def preprocess(self, file_path, sep=",", encoding="utf-8"):
        """ Preprocessing dataset """
        df = pd.read_csv(file_path, sep=sep, encoding=encoding)

        # kolom harus sesuai, cek jika terdapat kolom yang diperlukan
        required_columns = {"text", "emotion"}
        if not required_columns.issubset(df.columns):
            raise ValueError(
                f"File CSV harus memiliki kolom: {', '.join(required_columns)}")

        # drop duplikat untuk contentSnippet
        df.drop_duplicates(subset=["text"], inplace=True)

        df.dropna(subset=["text", "emotion"], inplace=True)

        df['text'] = df['text'].str.replace('"', "'")

        return df

    def process(self, file_path, sep=",", encoding="utf-8"):
        """ Preprocessing dataset """
        df = pd.read_csv(file_path, sep=sep, encoding=encoding)

        # Tambahkan kolom preprocessing text
        df["preprocessed_result"] = df["text"].apply(
            self.text_preprocessor.preprocess)

        df.drop_duplicates(subset=["preprocessed_result"], inplace=True)
        df.dropna(subset=["preprocessed_result"], inplace=True)

        return df

    def raw_formatter(self, file_path="./app/dataCollection/komentar.csv"):
        # Baca file Excel
        df = pd.read_excel(file_path)

        # Ganti tanda petik dua dalam kolom contentSnippet menjadi petik satu
        df['text'] = df['text'].str.replace('"', "'")

        df.drop_duplicates(subset=["text"], inplace=True)
        df.dropna(subset=["text"], inplace=True)

        # Simpan sebagai CSV dengan format yang benar
        df.to_csv("./preprocessing_results/new_dataset.csv",
                  index=False, quoting=csv.QUOTE_NONNUMERIC, encoding="utf-8")


if __name__ == "__main__":
    preprocessor = DatasetPreprocessor()
    preprocessor.raw_formatter()