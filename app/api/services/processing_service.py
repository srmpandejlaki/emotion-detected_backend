from sqlalchemy.orm import Session
from typing import List
from app.database.models.model_database import (
    DataCollection, ProcessResult, EmotionLabel,
    Model, ModelData, ConfusionMatrix, ClassMetrics
)
from app.database.schemas import (
    ProcessingResponse, ConfusionMatrixEntry,
    EmotionPredictionMetrics, UpdateManualLabelRequest,
    UpdatePredictedLabelRequest, ProcessResultResponse
)
from fastapi import HTTPException


def update_manual_emotion_service(db: Session, req: UpdateManualLabelRequest):
    data = db.query(DataCollection).filter(DataCollection.id_data == req.id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Data tidak ditemukan")

    label = db.query(EmotionLabel).filter(EmotionLabel.emotion_name == req.new_emotion).first()
    if not label:
        raise HTTPException(status_code=404, detail="Label emosi tidak ditemukan")

    data.id_label = label.id_label
    db.commit()

    return {"message": "Label manual berhasil diperbarui"}


def update_predicted_emotion_service(db: Session, req: UpdatePredictedLabelRequest):
    process = db.query(ProcessResult).filter(ProcessResult.id_data == req.id).first()
    if not process:
        raise HTTPException(status_code=404, detail="Data tidak ditemukan di hasil preprocessing")

    process.automatic_emotion = req.new_emotion
    db.commit()

    return {"message": "Label prediksi berhasil diperbarui"}


def get_all_processing_data_service(db: Session, page: int, limit: int):
    offset = (page - 1) * limit
    query = (
        db.query(DataCollection)
        .join(ProcessResult, DataCollection.id_data == ProcessResult.id_data)
        .outerjoin(EmotionLabel, DataCollection.id_label == EmotionLabel.id_label)
        .add_columns(
            DataCollection.id_data,
            DataCollection.text_data,
            ProcessResult.text_preprocessing,
            EmotionLabel.emotion_name,
            ProcessResult.automatic_emotion,
            ProcessResult.is_processed,
            ProcessResult.processed_at
        )
        .offset(offset)
        .limit(limit)
    )
    results = query.all()

    total = db.query(DataCollection).count()

    data = []
    for row in results:
        data.append({
            "id_data": row.id_data,
            "text_data": row.text_data,
            "text_preprocessing": row.text_preprocessing,
            "emotion": row.emotion_name,
            "automatic_emotion": row.automatic_emotion,
            "is_processed": row.is_processed,
            "processed_at": row.processed_at
        })

    return {
        "total": total,
        "data": data
    }


def evaluate_model_service(db: Session, test_size: float) -> ProcessingResponse:
    # Di sini diasumsikan bahwa evaluasi sudah dilakukan dan hasilnya disimpan
    model = db.query(Model).order_by(Model.id_model.desc()).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model belum dilatih")

    confusion = db.query(ConfusionMatrix).filter(ConfusionMatrix.matrix_id == model.matrix_id).all()
    metrics = db.query(ClassMetrics).filter(ClassMetrics.metrics_id == model.metrics_id).all()

    confusion_matrix = [
        ConfusionMatrixEntry(
            label_id=cm.label_id,
            predicted_label_id=cm.predicted_label_id,
            total=cm.total
        ) for cm in confusion
    ]

    precision_recall = [
        EmotionPredictionMetrics(
            label_id=met.label_id,
            precision=met.precision,
            recall=met.recall
        ) for met in metrics
    ]

    return ProcessingResponse(
        accuracy=model.accuracy,
        confusion_matrix=confusion_matrix,
        metrics=precision_recall
    )


def retrain_model_service(db: Session):
    # Placeholder untuk proses retraining, di sini bisa kamu integrasikan model Naive Bayes
    # Setelah selesai dilatih, kamu harus simpan akurasi, confusion matrix, dan metrics-nya ke Model, ConfusionMatrix, dan ClassMetrics

    # Contoh dummy untuk response
    return {"message": "Model berhasil dilatih ulang"}
