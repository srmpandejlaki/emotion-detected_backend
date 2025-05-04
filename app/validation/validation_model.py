from sqlalchemy.orm import Session

from app.database.schemas import ValidationResultCreate, ValidationResultResponse
from app.processing.algorithm.classification import naive_bayes_predict
from app.utils.evaluation_model import evaluate_model
from app.utils.label_utils import get_label_id_map
from app.api.services.validation_service import (
    get_model_by_id,
    get_untrained_process_results,
    save_confusion_matrix_entries,
    save_class_metrics_entries,
    create_validation_result,
    add_validation_data_entries,
    add_model_data_entries,
)


def perform_validation(payload: ValidationResultCreate, db: Session) -> ValidationResultResponse:
    model = get_model_by_id(payload.model_id, db)
    if not model:
        raise ValueError("Model not found")

    trained_process_ids = [md.id_process for md in model.model_data]

    test_data = get_untrained_process_results(trained_process_ids, db)
    if not test_data:
        raise ValueError("No validation data available")

    true_labels = []
    predicted_labels = []
    correct_flags = []

    for data in test_data:
        predicted = naive_bayes_predict(data.text_preprocessing, db)
        if predicted is None:
            raise ValueError(f"Prediction failed for process ID {data.id_process}")
        predicted_labels.append(predicted)
        true_label = data.automatic_emotion
        true_labels.append(true_label)
        correct_flags.append(predicted == true_label)

    evaluation_result = evaluate_model(true_labels, predicted_labels)
    label_id_map = get_label_id_map(db)

    matrix_id = save_confusion_matrix_entries(evaluation_result, label_id_map, db)
    metrics_id = save_class_metrics_entries(evaluation_result, label_id_map, db)

    validation_result = create_validation_result(
        model_id=payload.model_id,
        accuracy=evaluation_result["accuracy"],
        matrix_id=matrix_id,
        metrics_id=metrics_id,
        db=db
    )

    add_validation_data_entries(validation_result.id_validation, test_data, correct_flags, db)
    add_model_data_entries(payload.model_id, test_data, db)

    db.commit()

    return ValidationResultResponse(
        id_validation=validation_result.id_validation,
        model_id=payload.model_id,
        accuracy=validation_result.accuracy,
        matrix_id=validation_result.matrix_id,
        metrics_id=validation_result.metrics_id
    )
