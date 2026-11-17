import csv
from pathlib import Path
from src.detection.risk_scoring import calculate_risk_score
from src.detection.model_evaluation import evaluate_model

from src.detection.fraud_rules import (
    check_high_value,
    check_unknown_device,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = PROJECT_ROOT / "data" / "raw" / "transactions_large.csv"
print("CSV file location:", CSV_PATH)
print("File exists:", CSV_PATH.exists())
print("File size:", CSV_PATH.stat().st_size, "bytes")


def load_transactions() -> list[dict[str, str | int]]:
    with CSV_PATH.open(mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        print("CSV headers:", reader.fieldnames)
        transactions = list(reader)

    for transaction in transactions:
        transaction["amount"] = int(transaction["amount"])

    return transactions



if __name__ == "__main__":
    transactions = load_transactions()

    flagged_transactions = []
    all_predictions = []

    for transaction in transactions:
        result = calculate_risk_score(transaction)
        all_predictions.append(result)

        if result["risk_score"] > 0:
            flagged_transactions.append(result)

    print("\nFRAUDLENS AI - DETECTION REPORT")
    print("--------------------------------")
    print("Total transactions:", len(transactions))
    print("Flagged transactions:", len(flagged_transactions))
    print("Low-risk transactions:", len(transactions) - len(flagged_transactions))

    flagged_transactions.sort(
        key=lambda transaction: transaction["risk_score"],
        reverse=True,
    )

    print("\nTOP 10 FLAGGED TRANSACTIONS")
    print("--------------------------------")

    for transaction in flagged_transactions[:10]:
        print(
            f"{transaction['transaction_id']} | "
            f"Risk Score: {transaction['risk_score']}/100 | "
            f"Reasons: {', '.join(transaction['risk_reasons'])}"
        )

    evaluation = evaluate_model(transactions, all_predictions)

    print("\nMODEL EVALUATION")
    print("--------------------------------")
    print("True Positives:", evaluation["true_positives"])
    print("False Positives:", evaluation["false_positives"])
    print("True Negatives:", evaluation["true_negatives"])
    print("False Negatives:", evaluation["false_negatives"])
    print("Precision:", round(evaluation["precision"], 2))
    print("Recall:", round(evaluation["recall"], 2))
    print("F1-Score:", round(evaluation["f1_score"], 2))
