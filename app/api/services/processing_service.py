from sqlalchemy.orm import Session
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_recall_fscore_support
)
import uuid
from app.database.model_database import (
    DataCollection,
    ProcessResult,
    Model,
    ModelData,
    ConfusionMatrix,
    ClassMetrics
)

def get_preprocessed_data(db: Session):
    """
    Mengambil data yang sudah dipreprocessing beserta label asli dari DataCollection,
    dan menyertakan id_process dari masing-masing data.
    """
    results = (
        db.query(
            ProcessResult.id_process,
            ProcessResult.text_preprocessing,
            DataCollection.label_id
        )
        .join(DataCollection, ProcessResult.id_data == DataCollection.id_data)
        .all()
    )

    ids = [result.id_process for result in results]
    texts = [result.text_preprocessing for result in results]
    labels = [result.label_id for result in results]
    
    return ids, texts, labels


def delete_model_by_id(db: Session, model_id: int):
    model = db.query(Model).filter(Model.id_model == model_id).first()
    if model:
        db.delete(model)
        db.commit()
        return {"message": f"Model dengan ID {model_id} sudah dihapus."}
    return {"error": f"Model dengan ID {model_id} tidak ditemukan."}


def train_model(db: Session, ratio: float):
    # Ambil data preprocessed beserta label dan ID-nya
    ids, texts, labels = get_preprocessed_data(db)

    # Lakukan split
    X_train, X_test, y_train, y_test, id_train, id_test = train_test_split(
        texts, labels, ids, test_size=(1 - ratio), random_state=42, stratify=labels
    )

    # Latih model Naive Bayes
    model = MultinomialNB()
    model.fit(X_train, y_train)

    # Prediksi dan evaluasi
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision, recall, _, _ = precision_recall_fscore_support(y_test, y_pred, average=None, labels=sorted(set(labels)))

    # Simpan ke tabel Model
    new_model = Model(ratio_data=f"{int(ratio * 100)}:{int((1 - ratio) * 100)}", accuracy=accuracy)
    db.add(new_model)
    db.commit()
    db.refresh(new_model)

    model_id = new_model.id_model

    # Simpan ke model_data dan validation_data
    for idp in id_train:
        db.add(ModelData(id_model=model_id, id_process=idp))
    for idp, yt, yp in zip(id_test, y_test, y_pred):
        is_correct = yt == yp
        from app.models import ValidationResult, ValidationData  # Import lokal untuk hindari circular
        # Simpan hanya sekali per model
        val_result = ValidationResult(model_id=model_id, accuracy=accuracy)
        db.add(val_result)
        db.commit()
        db.refresh(val_result)

        db.add(ValidationData(id_validation=val_result.id_validation, id_process=idp, is_correct=is_correct))

    # Simpan class metrics
    unique_labels = sorted(set(labels))
    metrics_id = uuid.uuid4().int >> 64  # ID acak
    for i, label_id in enumerate(unique_labels):
        metric = ClassMetrics(metrics_id=metrics_id, label_id=label_id, precision=precision[i], recall=recall[i])
        db.add(metric)

    # Simpan confusion matrix
    matrix = confusion_matrix(y_test, y_pred, labels=unique_labels)
    matrix_id = uuid.uuid4().int >> 64  # ID acak
    for true_idx, true_label in enumerate(unique_labels):
        for pred_idx, pred_label in enumerate(unique_labels):
            count = int(matrix[true_idx][pred_idx])
            cm = ConfusionMatrix(matrix_id=matrix_id, label_id=true_label, predicted_label_id=pred_label, total=count)
            db.add(cm)

    # Update model dengan ID metrics dan confusion matrix
    new_model.metrics_id = metrics_id
    new_model.matrix_id = matrix_id
    db.commit()

    return {
        "model_id": model_id,
        "accuracy": accuracy,
        "metrics_id": metrics_id,
        "matrix_id": matrix_id
    }
