from sqlalchemy.orm import Session
from app.database.model_database import DataCollection, ProcessResult
from typing import List
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download resource jika belum ada
nltk.download("punkt")
nltk.download("stopwords")


def get_all_data_collection(db: Session) -> List[DataCollection]:
    return db.query(DataCollection).all()


def run_preprocessing(text: str) -> str:
    stop_words = set(stopwords.words("indonesian"))
    words = word_tokenize(text)
    filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    return " ".join(filtered_words)


def save_preprocessed_data(db: Session, processed_data: List[dict]):
    for item in processed_data:
        new_result = ProcessResult(
            id_data=item["id_data"],
            text_preprocessing=item["text_preprocessing"],
            is_training_data=True,  # default True, bisa diatur sesuai kebutuhan
            automatic_label=None
        )
        db.add(new_result)
    db.commit()
    return {"message": "Preprocessed data saved successfully"}


def get_all_preprocessing_results(db: Session):
    return db.query(ProcessResult).all()


def add_preprocessing_result(db: Session, id_data: int, text_preprocessing: str):
    result = ProcessResult(
        id_data=id_data,
        text_preprocessing=text_preprocessing,
        is_training_data=True,
        automatic_label=None
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result
