"""Document #10: FNS application/explanation (Заявление-пояснение в ФНС)."""

from dataclasses import dataclass


@dataclass
class FnsApplicationData:
    """Form data for the FNS application document."""

    # Applicant
    applicant_name: str = ""
    applicant_inn: str = ""
    applicant_address: str = ""
    applicant_phone: str = ""

    # FNS office
    fns_office: str = ""

    # Application details
    application_type: str = "пояснение"
    subject: str = ""
    details: str = ""
    application_date: str = ""  # YYYY-MM-DD

    @property
    def version(self) -> str:
        return "1.0.0"
