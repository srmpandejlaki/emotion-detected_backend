import pandas as pd
from joblib import dump
from sqlalchemy.orm import Session
from app.processing.algorithm.naive_bayes import NaiveBayesClassifier
from sklearn.model_selection import train_test_split
import time, os

MODEL_PATH = "./app/models/naive_bayes_model.pkl"
TEST_SIZE = 0.3

def load_data_from_db(db: Session):
    query = db.query(
        ProcessResult.text_preprocessing,
        EmotionLabel.emotion_name
    ).join(
        DataCollection,
        ProcessResult.id_data == DataCollection.id_data
    ).join(
        EmotionLabel,
        DataCollection.id_label == EmotionLabel.id_label
    ).filter(
        ProcessResult.text_preprocessing.isnot(None)
    )
    
    records = query.all()
    
    texts = [r.text_preprocessing for r in records]
    labels = [r.emotion_name for r in records]
    ids = [i for i in range(len(records))]  # Generate dummy IDs
    
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
        ids = list(range(len(df)))
        return texts, labels, ids
        
    start = time.time()

    # Pilih salah satu metode pengambilan data
    use_database = True  # Ganti ke False jika ingin menggunakan CSV
    
    if use_database:
        from app.database.config import SessionLocal
        from app.database.models.model_database import ProcessResult, DataCollection, EmotionLabel
        
        db = SessionLocal()
        try:
            texts, labels, ids = load_data_from_db(db)
        finally:
            db.close()
    else:
        dataset_path = "./data/preprocessing_results/new_dataset_preprocessed.csv"
        texts, labels, ids = load_data_from_csv(dataset_path)

    model, X_test, y_test, id_test = train_and_save_model(texts, labels, ids)
    evaluate_model(model, X_test, y_test, id_test)

    print(f"\nSelesai dalam {time.time() - start:.2f} detik")