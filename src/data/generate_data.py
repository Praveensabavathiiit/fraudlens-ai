import csv
import random
from pathlib import Path
from datetime import datetime, timedelta

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "transactions_large.csv"

CUSTOMERS = [f"CUST{i:03d}" for i in range(1, 101)]

LOCATIONS = ["Hyderabad", "Mumbai", "Delhi", "Bengaluru", "London"]

DEVICES = ["Mobile", "Laptop", "Tablet", "Unknown"]


def generate_suspicious_transactions() -> list[dict]:
    suspicious_start_time = datetime(2026, 3, 1)
    suspicious_transactions = []

    for i in range(1, 11):
        transaction = {
            "transaction_id": f"FRAUD{i:03d}",
            "customer_id": "CUST001",
            "amount": random.randint(100000, 200000),
            "location": "London",
            "device": "Unknown",
            "timestamp": (
                suspicious_start_time + timedelta(minutes=i * 5)
            ).isoformat(),
            "scenario_type": "high_value_unknown_device",
        }
        suspicious_transactions.append(transaction)

    return suspicious_transactions


def generate_transactions(total: int = 1000) -> list[dict]:
    transactions = []

    start_time = datetime(2026, 1, 1)

    for i in range(1, total + 1):
        transaction = {
            "scenario_type": "normal",
            "transaction_id": f"TXN{i:06d}",
            "customer_id": random.choice(CUSTOMERS),
            "amount": random.randint(100, 45000),
"device": random.choice(["Mobile", "Laptop", "Tablet"]),
            "location": random.choice(LOCATIONS),
            
            "timestamp": (
                start_time + timedelta(minutes=random.randint(0, 100000))
            ).isoformat(),
        }

        transactions.append(transaction)

    return transactions


def save_transactions(transactions: list[dict]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "scenario_type",
        "transaction_id",
        "customer_id",
        "amount",
        "location",
        "device",
        "timestamp",
    ]

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transactions)

if __name__ == "__main__":
    suspicious_transactions = generate_suspicious_transactions()

    normal_transactions = generate_transactions(
        1000 - len(suspicious_transactions)
    )

    all_transactions = normal_transactions + suspicious_transactions

    random.shuffle(all_transactions)

    save_transactions(all_transactions)

    print("Synthetic data generation completed!")
    print("Total transactions:", len(all_transactions))
    print("Normal transactions:", len(normal_transactions))
    print("Suspicious test transactions:", len(suspicious_transactions))