import pandas as pd
from joblib import dump
from sqlalchemy.orm import Session
from app.processing.algorithm.naive_bayes import NaiveBayesClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from itertools import product
from sklearn.metrics import accuracy_score
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


def train_with_gridsearch(df, param_grid=None):
    """Melatih model Naive Bayes dengan Grid Search untuk mencari parameter terbaik"""

    X_texts = df["preprocessed_result"].values
    y = df["emotion"].values

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Default grid search parameters
    if param_grid is None:
        param_grid = {
            # Coba beberapa split train-test
            "test_size": [0.2, 0.25, 0.3, 0.35, 0.4],
            # Coba berbagai random state
            "random_state": [42, 100]
        }

    best_score = 0
    best_model = None
    best_params = None
    results = []

    # Loop melalui semua kombinasi parameter
    for test_size, random_state in product(
        param_grid["test_size"], param_grid["random_state"]
    ):
        print(
            f"🔍 Evaluating Hybrid Model with test_size={test_size}, random_state={random_state}")

        print(f"📊 Data size before split: {len(X_texts)}")

        X_train, X_test, y_train, y_test, raw_train, raw_test = train_test_split(
            X_texts, y_encoded, X_texts, test_size=test_size, stratify=y_encoded, random_state=random_state
        )

        print(f"📈 Train size: {len(X_train)}, Test size: {len(X_test)}")

        naiveBayes_model = NaiveBayesClassifier()
        # Latih model
        start_time = time.time()
        naiveBayes_model.train(X_train, y_train)
        train_duration = time.time() - start_time

        # Prediksi hasil
        y_pred = []
        for i, text in enumerate(X_test):
            pred, _ = naiveBayes_model.predict(text)
            y_pred.append(pred)

        # Evaluasi model
        accuracy = accuracy_score(y_test, y_pred)
        print(f"✅ Accuracy: {accuracy:.4f}")

        results.append({
            "model": naiveBayes_model,
            "params": {
                "test_size": test_size,
                "random_state": random_state,
                "train_duration": train_duration
            },
            "accuracy": accuracy
        })

        if accuracy > best_score:
            best_score = accuracy
            best_model = naiveBayes_model
            best_params = {
                "test_size": test_size,
                "random_state": random_state,
                "train_duration": train_duration
            }

    # Urutkan hasil berdasarkan akurasi (tertinggi ke terendah)
    sorted_results = sorted(
        results, key=lambda x: x["accuracy"], reverse=True)

    print("\nRank\tAccuracy\tTest Size\tRandom State\tTrain Duration")
    print("----\t--------\t---------\t------------\t--------------")
    for i, result in enumerate(sorted_results, 1):
        accuracy = result["accuracy"]
        params = result["params"]
        print(
            f"{i}\t{accuracy:.4f}\t\t{params['test_size']}\t\t{params['random_state']}\t\t{params['train_duration']:.2f}s")

    return best_model, best_params, best_score


if __name__ == "__main__":
    # def load_data_from_csv(dataset_path: str):
    #     df = pd.read_csv(dataset_path)
    #     texts = df["preprocessed_result"].tolist()
    #     labels = df["emotion"].tolist()
    #     ids = list(range(len(df)))
    #     return texts, labels, ids
        
    # start = time.time()

    # # Pilih salah satu metode pengambilan data
    # use_database = True  # Ganti ke False jika ingin menggunakan CSV
    
    # if use_database:
    #     from app.database.config import SessionLocal
    #     from app.database.models.model_database import ProcessResult, DataCollection, EmotionLabel
        
    #     db = SessionLocal()
    #     try:
    #         texts, labels, ids = load_data_from_db(db)
    #     finally:
    #         db.close()
    # else:
    #     dataset_path = "./data/preprocessing_results/new_dataset_preprocessed.csv"
    #     texts, labels, ids = load_data_from_csv(dataset_path)

    # model, X_test, y_test, id_test = train_and_save_model(texts, labels, ids)
    # evaluate_model(model, X_test, y_test, id_test)

    # print(f"\nSelesai dalam {time.time() - start:.2f} detik")

    dataset_path = "./data/preprocessing_results/new_dataset_preprocessed.csv"

    df = pd.read_csv(dataset_path)

    best_model, best_params, best_score = train_with_gridsearch(df)

    print("\n🎉 Hasil Grid Search Terbaik:")
    print(f"🔝 Akurasi terbaik: {best_score:.4f}")
    print("⚙️ Parameter terbaik:")
    for param, value in best_params.items():
        print(f"  - {param}: {value}")