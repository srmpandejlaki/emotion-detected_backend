from sqlalchemy.orm import Session
from app.database.model_database import (
    Model, ProcessResult, ConfusionMatrix,
    ClassMetrics, ValidationResult, ValidationData,
    ModelData
)


def get_model_by_id(model_id: int, db: Session):
    return db.query(Model).filter_by(id_model=model_id).first()


def get_untrained_process_results(trained_ids: list[int], db: Session):
    return db.query(ProcessResult).filter(
        ProcessResult.is_processed == True,
        ~ProcessResult.id_process.in_(trained_ids)
    ).all()


def save_confusion_matrix_entries(evaluation_result: dict, label_id_map: dict, db: Session) -> int:
    matrix_id = None
    for actual_row in evaluation_result["confusion_matrix"]["matrix"]:
        actual_label = actual_row["actual"]
        actual_id = label_id_map.get(actual_label)
        for predicted_label, total in actual_row.items():
            if predicted_label == "actual":
                continue
            predicted_id = label_id_map.get(predicted_label)
            matrix = ConfusionMatrix(
                label_id=actual_id,
                predicted_label_id=predicted_id,
                total=total
            )
            db.add(matrix)
            if matrix_id is None:
                db.flush()
                matrix_id = matrix.matrix_id
    return matrix_id


def save_class_metrics_entries(evaluation_result: dict, label_id_map: dict, db: Session) -> int:
    metrics_id = None
    for label, precision in evaluation_result["precision"].items():
        recall = evaluation_result["recall"].get(label, 0.0)
        metric = ClassMetrics(
            label_id=label_id_map.get(label),
            precision=precision,
            recall=recall
        )
        db.add(metric)
        if metrics_id is None:
            db.flush()
            metrics_id = metric.metrics_id
    return metrics_id


def create_validation_result(model_id: int, accuracy: float, matrix_id: int, metrics_id: int, db: Session):
    result = ValidationResult(
        model_id=model_id,
        accuracy=accuracy,
        matrix_id=matrix_id,
        metrics_id=metrics_id
    )
    db.add(result)
    db.flush()
    return result


def add_validation_data_entries(validation_id: int, test_data: list, correct_flags: list[bool], db: Session):
    for idx, data in enumerate(test_data):
        db.add(ValidationData(
            id_validation=validation_id,
            id_process=data.id_process,
            is_correct=correct_flags[idx]
        ))


def add_model_data_entries(model_id: int, test_data: list, db: Session):
    for data in test_data:
        db.add(ModelData(
            id_model=model_id,
            id_process=data.id_process
        ))
