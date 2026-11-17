from src.detection.risk_scoring import calculate_risk_score


def test_high_value_unknown_device():
    transaction = {
        "transaction_id": "TEST001",
        "amount": 100000,
        "device": "Unknown",
    }

    result = calculate_risk_score(transaction)

    assert result["risk_score"] == 70
    assert "High-value transaction" in result["risk_reasons"]
    assert "Unknown device" in result["risk_reasons"]


def test_low_value_known_device():
    transaction = {
        "transaction_id": "TEST002",
        "amount": 5000,
        "device": "Mobile",
    }

    result = calculate_risk_score(transaction)

    assert result["risk_score"] == 0
    assert result["risk_reasons"] == []