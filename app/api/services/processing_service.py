import joblib
from sqlalchemy.orm import Session
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support
from app.database.model_database import ProcessResult, Model, ModelData, ConfusionMatrix, ClassMetrics
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

def train_model(ratio_str: str, db: Session):
    ratio = RATIO_MAP.get(ratio_str)
    if ratio is None:
        raise ValueError("Rasio tidak valid. Pilih dari 60:40, 70:30, 80:20")

    data = db.query(ProcessResult).filter(ProcessResult.is_training_data == True).all()
    if not data:
        return None, "Tidak ada data training."

    texts = [d.text_preprocessing for d in data]
    labels = [d.automatic_label for d in data]
    ids = [d.id_process for d in data]

    X_train, X_test, y_train, y_test, id_train, id_test = train_test_split(
        texts, labels, ids, test_size=ratio, stratify=labels, random_state=42
    )

    manual_nb = ManualNaiveBayes()
    manual_nb.fit(X_train, y_train)

    joblib.dump(manual_nb, MODEL_PATH)
    joblib.dump(manual_nb.vectorizer, VECTORIZER_PATH)

    # Inisialisasi hanya sekali saat dibutuhkan
    fallback_classifier = BERTEmotionClassifier()

    y_pred = []
    for text in X_test:
        prob_dict = manual_nb.predict_proba(text)
        top_probs = sorted(prob_dict.items(), key=lambda x: x[1], reverse=True)

        if len(top_probs) >= 2 and top_probs[0][1] == top_probs[1][1]:
            fallback_label = fallback_classifier.combined_score(text)
            y_pred.append(fallback_label)
        else:
            y_pred.append(top_probs[0][0])

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="macro", zero_division=0)
    recall = recall_score(y_test, y_pred, average="macro", zero_division=0)

    model_record = Model(
        ratio_data=ratio_str,
        accuracy=accuracy,
        matrix_id=None,
        metrics_id=None
    )
    db.add(model_record)
    db.commit()
    db.refresh(model_record)

    for id_process in id_train:
        model_data = ModelData(id_model=model_record.id_model, id_process=id_process)
        db.add(model_data)

    cm = confusion_matrix(y_test, y_pred)
    unique_labels = sorted(list(set(y_test) | set(y_pred)))
    matrix_id = model_record.id_model
    for i, true_label in enumerate(unique_labels):
        for j, pred_label in enumerate(unique_labels):
            db.add(ConfusionMatrix(
                matrix_id=matrix_id,
                label_id=true_label,
                predicted_label_id=pred_label,
                total=int(cm[i][j])
            ))

    precisions, recalls, _, _ = precision_recall_fscore_support(y_test, y_pred, labels=unique_labels, zero_division=0)
    metrics_id = model_record.id_model

    for label, prec, rec in zip(unique_labels, precisions, recalls):
        db.add(ClassMetrics(
            metrics_id=metrics_id,
            label_id=label,
            precision=prec,
            recall=rec
        ))

    model_record.matrix_id = matrix_id
    model_record.metrics_id = metrics_id
    db.commit()

    return {
        "model_id": model_record.id_model,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall
    }, None
