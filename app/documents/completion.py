"""Document #2: Completion certificate (Акт выполненных работ)."""

from dataclasses import dataclass


@dataclass
class CompletionData:
    """Form data for the completion certificate document."""

    # Parties
    performer_name: str = ""
    performer_inn: str = ""
    performer_address: str = ""
    customer_name: str = ""
    customer_inn: str = ""
    customer_address: str = ""

    # Work details
    contract_number: str = ""
    contract_date: str = ""  # YYYY-MM-DD
    work_description: str = ""
    work_amount: float = 0.0
    work_date: str = ""  # YYYY-MM-DD

    @property
    def version(self) -> str:
        return "1.0.0"
