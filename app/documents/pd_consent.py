"""Document #9: Personal data processing consent (Согласие на обработку ПДн)."""

from dataclasses import dataclass


@dataclass
class PdConsentData:
    """Form data for the personal data processing consent document."""

    # Subject
    subject_full_name: str = ""
    subject_passport: str = ""
    subject_inn: str = ""
    subject_address: str = ""
    subject_phone: str = ""
    subject_email: str = ""

    # Operator
    operator_name: str = ""
    operator_address: str = ""

    # Consent details
    purposes: str = ""
    data_types: str = ""
    consent_period: str = "3 года"
    consent_date: str = ""  # YYYY-MM-DD

    @property
    def version(self) -> str:
        return "1.0.0"
