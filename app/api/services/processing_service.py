from sqlalchemy.orm import Session
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report, confusion_matrix
from app.database import model_database

def get_unprocessed_data(db: Session):
    return db.query(model_database.ProcessResult).filter(
        model_database.ProcessResult.is_processed == False
    ).all()

def mark_data_as_processed(db: Session, data_ids: list[int]):
    db.query(model_database.ProcessResult).filter(
        model_database.ProcessResult.id_process.in_(data_ids)
    ).update({
        model_database.ProcessResult.is_processed: True,
        model_database.ProcessResult.processed_at: datetime.now()
    }, synchronize_session=False)
    db.commit()

def save_model_and_metrics(db: Session, report: dict, matrix: list[list[int]]):
    model_entry = model_database.Model(
        model_name="Naive Bayes",
        trained_at=datetime.now()
    )
    db.add(model_entry)
    db.commit()
    db.refresh(model_entry)

    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            db.add(model_database.ConfusionMatrix(
                model_id=model_entry.id_model,
                actual_class=i,
                predicted_class=j,
                count=val
            ))

    for label, metrics in report.items():
        if label not in ["accuracy", "macro avg", "weighted avg"]:
            db.add(model_database.ClassMetrics(
                model_id=model_entry.id_model,
                emotion_label=str(label),
                precision=metrics.get("precision"),
                recall=metrics.get("recall")
            ))

    db.commit()

def train_from_new_data(db: Session):
    new_data = get_unprocessed_data(db)
    if not new_data:
        return {"message": "Tidak ada data baru yang belum diproses."}

    texts, labels, id_process_list = [], [], []

    for item in new_data:
        if item.text_preprocessing:
            # Ambil label dari tabel DataCollection berdasarkan id_data
            data = db.query(model_database.DataCollection).filter(
                model_database.DataCollection.id_data == item.id_data
            ).first()
            if data and data.label_id is not None:
                texts.append(item.text_preprocessing)
                labels.append(data.label_id)
                id_process_list.append(item.id_process)

    if not texts:
        return {"message": "Data baru belum lengkap untuk dilatih."}

    # Latih model dengan data baru
    vectorizer = CountVectorizer()
    X_train = vectorizer.fit_transform(texts)
    model = MultinomialNB()
    model.fit(X_train, labels)

    # Tandai data baru sebagai telah diproses
    mark_data_as_processed(db, id_process_list)

    # Ambil ulang semua data yang sudah diproses untuk evaluasi keseluruhan
    all_processed = db.query(model_database.ProcessResult).filter(
        model_database.ProcessResult.is_processed == True,
        model_database.ProcessResult.text_preprocessing != None
    ).all()

    eval_texts, eval_labels = [], []

    for item in all_processed:
        data = db.query(model_database.DataCollection).filter(
            model_database.DataCollection.id_data == item.id_data
        ).first()
        if data and data.label_id is not None:
            eval_texts.append(item.text_preprocessing)
            eval_labels.append(data.label_id)

    X_eval = vectorizer.transform(eval_texts)
    y_pred = model.predict(X_eval)

    report = classification_report(eval_labels, y_pred, output_dict=True)
    matrix = confusion_matrix(eval_labels, y_pred)

    # Simpan model dan evaluasinya
    save_model_and_metrics(db, report, matrix)

    return {
        "message": "Model berhasil dilatih dari data baru.",
        "jumlah_data_baru": len(id_process_list),
        "jumlah_total_terproses": len(eval_labels),
        "evaluasi": report
    }

