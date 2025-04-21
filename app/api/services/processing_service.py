import joblib
from sqlalchemy.orm import Session
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support
from app.database.model_database import ProcessResult, Model, ModelData, ConfusionMatrix, ClassMetrics, LabelEmotion
from app.processing.algorithm.naiveBayes import ManualNaiveBayes
from app.processing.metrics.class_metrics import accuracy_score, precision_score, recall_score
from app.processing.metrics.confusion_matrix import confusion_matrix
from app.processing.alternatif_method.bert_lexicon import BERTEmotionClassifier  # Ganti ini sesuai nama file

MODEL_PATH = "app/models/models_ml/naive_bayes_manual_model.pkl"
VECTORIZER_PATH = "app/models/models_ml/vectorizer.pkl"

RATIO_MAP = {
    "60:40": 0.4,
    "70:30": 0.3,
    "80:20": 0.2
}

# Fungsi untuk mengambil data yang sudah dipreprocessing
def get_preprocessed_data(db: Session):
    data = db.query(ProcessResult).filter(ProcessResult.text_preprocessing != None).all()
    if not data:
        return None, None, None, "Tidak ada data yang sudah dipreprocessing."

    texts = [d.text_preprocessing for d in data]
    labels = [d.auto_label.id_label for d in data]  # pakai relasi ke LabelEmotion
    ids = [d.id_process for d in data]

    return texts, labels, ids, None

# Fungsi untuk menyimpan hasil model, confusion matrix, dan metrics ke dalam database
def save_model_result(db, ratio_str, accuracy, precision_dict, recall_dict, train_ids, y_test, y_pred, unique_labels):
    # 1. Simpan model
    model = Model(ratio_data=ratio_str, accuracy=accuracy)
    db.add(model)
    db.commit()
    db.refresh(model)

    # 2. Tandai data latih
    for id_process in train_ids:
        db.query(ProcessResult).filter(ProcessResult.id_process == id_process).update({
            ProcessResult.is_training_data: True
        })
        db.add(ModelData(id_model=model.id_model, id_process=id_process))

    # 3. Simpan confusion matrix
    matrix_id = model.id_model  # gunakan id_model sebagai matrix_id agar mudah
    for actual, predicted in zip(y_test, y_pred):
        actual_label = db.query(LabelEmotion).filter(LabelEmotion.nama_label == actual).first()
        pred_label = db.query(LabelEmotion).filter(LabelEmotion.nama_label == predicted).first()
        cm = db.query(ConfusionMatrix).filter_by(
            matrix_id=matrix_id,
            label_id=actual_label.id_label,
            predicted_label_id=pred_label.id_label
        ).first()

        if cm:
            cm.total += 1
        else:
            new_cm = ConfusionMatrix(
                matrix_id=matrix_id,
                label_id=actual_label.id_label,
                predicted_label_id=pred_label.id_label,
                total=1
            )
            db.add(new_cm)

    # 4. Simpan class metrics
    for label in unique_labels:
        label_obj = db.query(LabelEmotion).filter(LabelEmotion.nama_label == label).first()
        db.add(ClassMetrics(
            metrics_id=model.id_model,
            label_id=label_obj.id_label,
            precision=precision_dict.get(label, 0),
            recall=recall_dict.get(label, 0)
        ))

    db.commit()
    return model

# Fungsi untuk melatih model dan menyimpan hasilnya
def train_model(ratio_str: str, db: Session):
    ratio = RATIO_MAP.get(ratio_str)
    if ratio is None:
        raise ValueError("Rasio tidak valid. Pilih dari 60:40, 70:30, 80:20")

    texts, labels, ids, error = get_preprocessed_data(db)
    if error:
        return None, error

    # Pisahkan data latih dan data uji
    X_train, X_test, y_train, y_test, id_train, id_test = train_test_split(
        texts, labels, ids, test_size=ratio, stratify=labels, random_state=42
    )

    # Latih model Naive Bayes
    manual_nb = ManualNaiveBayes()
    manual_nb.fit(X_train, y_train)

    # Simpan model dan vectorizer
    joblib.dump(manual_nb, MODEL_PATH)
    joblib.dump(manual_nb.vectorizer, VECTORIZER_PATH)

    # Siapkan fallback classifier untuk BERT + Lexicon
    fallback_classifier = BERTEmotionClassifier()

    # Prediksi dengan fallback jika dua emosi memiliki probabilitas sama
    y_pred = []
    for text in X_test:
        prob_dict = manual_nb.predict_proba(text)
        top_probs = sorted(prob_dict.items(), key=lambda x: x[1], reverse=True)

        if len(top_probs) >= 2 and top_probs[0][1] == top_probs[1][1]:
            fallback_label = fallback_classifier.combined_score(text)
            y_pred.append(fallback_label)
        else:
            y_pred.append(top_probs[0][0])

    # Hitung accuracy, precision, dan recall
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="macro", zero_division=0)
    recall = recall_score(y_test, y_pred, average="macro", zero_division=0)

    # Simpan hasil model dan evaluasi ke database
    model = save_model_result(db, ratio_str, accuracy, {}, {}, id_train, y_test, y_pred, list(set(y_test + y_pred)))

    return {
        "model_id": model.id_model,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall
    }, None

# Fungsi untuk menghapus model berdasarkan ID
def delete_model_by_id(model_id: int, db: Session):
    model = db.query(Model).filter(Model.id_model == model_id).first()
    if not model:
        return False, "Model tidak ditemukan."

    db.query(ModelData).filter_by(id_model=model_id).delete()
    db.query(ConfusionMatrix).filter_by(matrix_id=model_id).delete()
    db.query(ClassMetrics).filter_by(metrics_id=model_id).delete()
    db.delete(model)
    db.commit()
    return True, "Model berhasil dihapus."
