"""Document #4: Receipt confirmation (Чек-подтверждение) with QR placeholder."""

from dataclasses import dataclass


@dataclass
class ReceiptData:
    """Form data for the receipt confirmation document."""

    # Issuer
    issuer_name: str = ""
    issuer_inn: str = ""
    issuer_address: str = ""

    # Payment details
    payment_date: str = ""  # YYYY-MM-DD
    amount: float = 0.0
    service_description: str = ""
    payment_method: str = "bank_transfer"

    @property
    def version(self) -> str:
        return "1.0.0"
