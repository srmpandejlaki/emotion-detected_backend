from sqlalchemy.orm import Session
from app.processing.train_model import load_data_from_db, train_and_save_model, evaluate_model
from app.database.models.model_database import Model, ModelData, ProcessResult, ConfusionMatrix, ClassMetrics
from app.database.schemas import TrainResultSchema
from datetime import datetime

def process_training(db: Session, ratio: str) -> TrainResultSchema:
    # 1. Load data dari DB
    texts, labels, ids = load_data_from_db(db)

    # 2. Update rasio jika frontend memberi input selain default
    test_size = 0.2  # default
    if ratio == "70:30":
        test_size = 0.3
    elif ratio == "60:40":
        test_size = 0.4

    # 3. Training model
    model, X_test, y_test, id_test = train_and_save_model(texts, labels, ids, test_size=test_size)

    # 4. Evaluasi model
    predictions, ambiguous, metrics = evaluate_model(model, X_test, y_test, id_test)

    # 5. Simpan ke tabel Model
    new_model = Model(
        ratio_data=ratio,
        accuracy=metrics["accuracy"],
    )
    db.add(new_model)
    db.commit()
    db.refresh(new_model)

    # 6. Simpan ke tabel ModelData
    for pid in ids:
        db.add(ModelData(id_model=new_model.id_model, id_process=pid))
    db.commit()

    # 7. Simpan confusion matrix
    for item in metrics["confusion_matrix"]:
        db.add(ConfusionMatrix(
            matrix_id=new_model.id_model,  # misalnya gunakan ID model sebagai matrix_id
            label_id=item["label_id"],
            predicted_label_id=item["predicted_id"],
            total=item["total"]
        ))
    db.commit()

    # 8. Simpan class metrics (precision/recall)
    for item in metrics["class_metrics"]:
        db.add(ClassMetrics(
            metrics_id=new_model.id_model,
            label_id=item["label_id"],
            precision=item["precision"],
            recall=item["recall"]
        ))
    db.commit()

    # 9. Update automatic_emotion ke tabel ProcessResult
    for pred in predictions:
        db.query(ProcessResult).filter(ProcessResult.id_process == pred["id"]).update({
            "automatic_emotion": pred["predicted_emotion"],
            "is_processed": True
        })
    db.commit()

    # 10. Untuk data ambigu → kirim ke metode BERT & leksikon (panggil modul lain)
    # ... (nanti kamu tinggal buat `run_bert_lexicon_prediction(ambiguous, db)`)

    return TrainResultSchema(
        model_id=new_model.id_model,
        accuracy=metrics["accuracy"],
        total_data=len(texts),
        ambiguous_count=len(ambiguous),
        ratio_used=ratio
    )
