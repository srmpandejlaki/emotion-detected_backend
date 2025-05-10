import pandas as pd
from joblib import dump
import Session
from app.api.services.preprocessing_service import get_all_preprocessing_results
from app.processing.algorithm.naive_bayes import NaiveBayesClassifier
from sklearn.model_selection import train_test_split
import time, os

MODEL_PATH = "./app/models/naive_bayes_model.pkl"
TEST_SIZE = 0.2

def load_data_from_db(db: Session):
    records = get_all_preprocessing_results(db)
    texts = [r.preprocessed_result for r in records]
    labels = [r.emotion for r in records]
    ids = [r.id_process for r in records]
    return texts, labels, ids

def train_and_save_model(texts, labels, ids):
    X_train, X_test, y_train, y_test, id_train, id_test = train_test_split(
        texts, labels, ids, test_size=TEST_SIZE, random_state=42
    )

    model = NaiveBayesClassifier()
    model.train(X_train, y_train)

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    dump(model, MODEL_PATH)
    print(f"✅ Model disimpan di: {MODEL_PATH}")

    return model, X_test, y_test, id_test

def evaluate_model(model, X_test, y_test, id_test):
    predictions, ambiguous, _ = model.get_ambiguous_predictions(X_test, y_test, id_test)
    benar = sum(1 for p in predictions if p["predicted_emotion"] == p["manual_emotion"])
    total = len(predictions)
    akurasi = benar / total if total > 0 else 0

    print(f"\nAkurasi: {akurasi * 100:.2f}%")
    print(f"Data dengan dua emosi probabilitas sama: {len(ambiguous)}")

if __name__ == "__main__":
    def load_data_from_csv(dataset_path: str):
        df = pd.read_csv(dataset_path)
        texts = df["preprocessed_result"].tolist()
        labels = df["emotion"].tolist()
        ids = df["id_process"].tolist()
        return texts, labels, ids
        
    start = time.time()

    # Ganti path CSV sesuai kebutuhanmu
    dataset_path = "./data/preprocessing_results/new_dataset_preprocessed.csv"
    texts, labels, ids = load_data_from_csv(dataset_path)

    model, X_test, y_test, id_test = train_and_save_model(texts, labels, ids)
    evaluate_model(model, X_test, y_test, id_test)

    print(f"\nSelesai dalam {time.time() - start:.2f} detik")
