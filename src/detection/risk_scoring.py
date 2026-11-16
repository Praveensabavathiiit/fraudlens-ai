def calculate_risk_score(transaction: dict) -> dict:
    score = 0
    reasons = []

    if transaction["amount"] > 50000:
        score += 40
        reasons.append("High-value transaction")

    if transaction["device"].lower() == "unknown":
        score += 30
        reasons.append("Unknown device")

    return {
        "transaction_id": transaction["transaction_id"],
        "risk_score": score,
        "risk_reasons": reasons,
    }