"""Document #3: Service contract (Договор возмездного оказания услуг)."""

from dataclasses import dataclass


@dataclass
class ServiceContractData:
    """Form data for the service contract document."""

    # Parties
    provider_name: str = ""
    provider_inn: str = ""
    provider_address: str = ""
    client_name: str = ""
    client_inn: str = ""
    client_address: str = ""

    # Contract details
    contract_number: str = ""
    contract_date: str = ""  # YYYY-MM-DD
    subject: str = ""
    price: float = 0.0
    term_start: str = ""  # YYYY-MM-DD
    term_end: str = ""  # YYYY-MM-DD
    payment_terms: str = ""

    @property
    def version(self) -> str:
        return "1.0.0"
