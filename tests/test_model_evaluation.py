
from src.detection.model_evaluation import evaluate_model


def test_evaluate_model_metrics():
    transactions = [
        {"transaction_id": "T001", "scenario_type": "high_value_unknown_device"},
        {"transaction_id": "T002", "scenario_type": "normal"},
        {"transaction_id": "T003", "scenario_type": "normal"},
        {"transaction_id": "T004", "scenario_type": "high_value_unknown_device"},
    ]

    predictions = [
        {"transaction_id": "T001", "risk_score": 70},  # True Positive
        {"transaction_id": "T002", "risk_score": 40},  # False Positive
        {"transaction_id": "T003", "risk_score": 0},   # True Negative
        {"transaction_id": "T004", "risk_score": 0},   # False Negative
    ]

    result = evaluate_model(transactions, predictions)

    assert result["true_positives"] == 1
    assert result["false_positives"] == 1
    assert result["true_negatives"] == 1
    assert result["false_negatives"] == 1

    assert result["precision"] == 0.5
    assert result["recall"] == 0.5
    assert result["f1_score"] == 0.5
