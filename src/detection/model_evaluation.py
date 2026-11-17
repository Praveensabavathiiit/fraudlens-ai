
def evaluate_model(transactions: list[dict], predictions: list[dict]) -> dict:
    actual_labels = {
        transaction["transaction_id"]: transaction["scenario_type"]
        == "high_value_unknown_device"
        for transaction in transactions
    }

    predicted_labels = {
        prediction["transaction_id"]: prediction["risk_score"] > 0
        for prediction in predictions
    }

    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0

    for transaction_id, actual in actual_labels.items():
        predicted = predicted_labels[transaction_id]

        if actual and predicted:
            true_positives += 1
        elif not actual and predicted:
            false_positives += 1
        elif not actual and not predicted:
            true_negatives += 1
        else:
            false_negatives += 1

    
    precision = (
        true_positives / (true_positives + false_positives)
        if true_positives + false_positives > 0
        else 0
    )

    recall = (
        true_positives / (true_positives + false_negatives)
        if true_positives + false_negatives > 0
        else 0
    )

    f1_score = (
        2 * precision * recall / (precision + recall)
        if precision + recall > 0
        else 0
    )

    return {
        "true_positives": true_positives,
        "false_positives": false_positives,
        "true_negatives": true_negatives,
        "false_negatives": false_negatives,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
    }
