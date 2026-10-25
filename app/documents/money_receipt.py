"""Document #6: Money receipt acknowledgment (Расписка в получении денег)."""

from dataclasses import dataclass


@dataclass
class MoneyReceiptData:
    """Form data for the money receipt acknowledgment document."""

    # Recipient (who received money)
    recipient_name: str = ""
    recipient_passport: str = ""
    recipient_address: str = ""

    # Payer
    payer_name: str = ""
    payer_passport: str = ""

    # Amount
    amount: float = 0.0
    amount_in_words: str = ""
    purpose: str = ""
    receipt_date: str = ""  # YYYY-MM-DD

    @property
    def version(self) -> str:
        return "1.0.0"
