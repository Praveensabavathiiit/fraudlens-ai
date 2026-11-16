def check_high_value(transaction: dict, threshold: int = 50000) -> bool:
    return transaction["amount"] > threshold


def check_unknown_device(transaction: dict) -> bool:
    return transaction["device"].lower() == "unknown"