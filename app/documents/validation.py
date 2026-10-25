"""Validation functions for document forms."""

import re
from datetime import datetime


def validate_inn(inn: str) -> bool:
    """Validate Russian INN (10 or 12 digits with check digit)."""
    if not re.match(r"^\d{10,12}$", inn):
        return False

    digits = [int(d) for d in inn]

    if len(digits) == 10:
        weights = [2, 4, 10, 3, 5, 9, 4, 6, 8]
        total = sum(d * w for d, w in zip(digits, weights))
        check = total % 11 % 10
        return check == digits[9]

    elif len(digits) == 12:
        weights1 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
        weights2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6]
        check1 = sum(d * w for d, w in zip(digits[:10], weights1)) % 11 % 10
        check2 = sum(d * w for d, w in zip(digits[:10], weights2)) % 11 % 10
        return check1 == digits[10] and check2 == digits[11]

    return False


def validate_bik(bik: str) -> bool:
    """Validate Russian BIK (9 digits)."""
    return bool(re.match(r"^\d{9}$", bik))


def validate_date(date_str: str) -> bool:
    """Validate YYYY-MM-DD date."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_phone(phone: str) -> bool:
    """Validate Russian phone number."""
    cleaned = re.sub(r"[\s\-\(\)]", "", phone)
    if cleaned.startswith("8"):
        cleaned = "7" + cleaned[1:]
    return bool(re.match(r"^7\d{10}$", cleaned))


def validate_amount(amount: str) -> bool:
    """Validate monetary amount (positive number with up to 2 decimals)."""
    return bool(re.match(r"^\d+(\.\d{1,2})?$", str(amount))) and float(amount) > 0
