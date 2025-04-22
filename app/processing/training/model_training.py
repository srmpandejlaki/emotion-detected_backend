from sqlalchemy.orm import Session
from datetime import datetime
from app.database.model_database import ProcessResult, DataCollection, Model, ModelData, ConfusionMatrix, ClassMetrics
from app.core.text_processing import preprocess_text
from app.processing.algorithm.naive_bayes import train_naive_bayes, predict_naive_bayes
from app.core.evaluation import calculate_confusion_matrix, calculate_metrics
from app.database.schemas import CreateModelSchema  # jika ada
from collections import defaultdict

def train_from_new_data(db: Session, ratio: float = 0.7):
    # Ambil data yang belum diproses (is_processed = False)
    new_data = db.query(ProcessResult).filter(ProcessResult.is_processed == False).all()
    if not new_data:
        return "Tidak ada data baru untuk diproses."

    # Ambil data training dan testing dari data baru
    texts = []
    labels = []
    ids = []
    for item in new_data:
        text = item.text_preprocessing
        dc = db.query(DataCollection).filter(DataCollection.id_data == item.id_data).first()
        if text and dc:
            texts.append(text)
            labels.append(dc.label_id)  # ambil dari DataCollection
            ids.append(item.id_process)

    if not texts:
        return "Data baru belum lengkap (text atau label kosong)."

    # Pisahkan data training dan testing
    split_index = int(len(texts) * ratio)
    train_texts, test_texts = texts[:split_index], texts[split_index:]
    train_labels, test_labels = labels[:split_index], labels[split_index:]
    test_ids = ids[split_index:]

    # Train model Naive Bayes (manual)
    model = train_naive_bayes(train_texts, train_labels)

    # Predict untuk data uji
    predictions = predict_naive_bayes(test_texts, model)

    # Simpan hasil prediksi
    for id_process, pred in zip(test_ids, predictions):
        pr = db.query(ProcessResult).filter(ProcessResult.id_process == id_process).first()
        if pr:
            pr.automatic_emotion = pred
            pr.is_processed = True
            pr.processed_at = datetime.now()

    # Tandai data training sebagai telah diproses
    train_ids = ids[:split_index]
    for id_process in train_ids:
        pr = db.query(ProcessResult).filter(ProcessResult.id_process == id_process).first()
        if pr:
            pr.is_processed = True
            pr.processed_at = datetime.now()

    db.commit()

    # Ambil semua hasil prediksi untuk evaluasi (lama + baru)
    processed = db.query(ProcessResult).filter(ProcessResult.is_processed == True).all()
    all_labels = []
    all_preds = []
    for p in processed:
        dc = db.query(DataCollection).filter(DataCollection.id_data == p.id_data).first()
        if dc and p.automatic_emotion:
            all_labels.append(dc.label_id)
            all_preds.append(p.automatic_emotion)

    # Hitung confusion matrix & metrics
    matrix = calculate_confusion_matrix(all_labels, all_preds)
    metrics = calculate_metrics(matrix)

    # Simpan hasil model ke tabel `model`
    model_entry = Model(
        ratio_data=ratio,
        accuracy=metrics['accuracy'],
    )
    db.add(model_entry)
    db.commit()
    db.refresh(model_entry)

    # Simpan matrix dan metrics ke tabel
    matrix_id = save_confusion_matrix(db, matrix, model_entry.id_model)
    metrics_id = save_class_metrics(db, metrics['precision'], metrics['recall'], model_entry.id_model)

    # Update foreign key di tabel model
    model_entry.matrix_id = matrix_id
    model_entry.metrics_id = metrics_id
    db.commit()

    # Simpan hubungan antara model dan data
    for id_process in train_ids + test_ids:
        link = ModelData(id_model=model_entry.id_model, id_process=id_process)
        db.add(link)

    db.commit()
    return f"Training selesai dengan akurasi {metrics['accuracy']*100:.2f}%"
