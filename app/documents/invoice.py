"""Document #1: Invoice (Счёт) for self-employed (НПД)."""

from dataclasses import dataclass
from typing import Literal


@dataclass
class InvoiceData:
    """Form data for the invoice document."""

    # Issuer (self-employed)
    issuer_name: str = ""
    issuer_inn: str = ""
    issuer_phone: str = ""
    issuer_address: str = ""

    # Recipient
    recipient_name: str = ""
    recipient_inn: str = ""
    recipient_address: str = ""

    # Invoice details
    invoice_number: str = ""
    invoice_date: str = ""  # YYYY-MM-DD
    service_description: str = ""
    service_amount: float = 0.0
    payment_method: Literal["bank_transfer", "cash"] = "bank_transfer"

    # Source indicators
    issuer_name_source: str = "manual"
    recipient_name_source: str = "manual"

    @property
    def version(self) -> str:
        return "1.0.0"
