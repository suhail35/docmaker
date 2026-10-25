"""Document #7: Loan contract between individuals (Договор займа между физлицами)."""

from dataclasses import dataclass


@dataclass
class LoanData:
    """Form data for the loan contract document."""

    # Lender
    lender_name: str = ""
    lender_passport: str = ""
    lender_address: str = ""

    # Borrower
    borrower_name: str = ""
    borrower_passport: str = ""
    borrower_address: str = ""

    # Loan details
    loan_amount: float = 0.0
    interest_rate: str = "без процентов"
    loan_date: str = ""  # YYYY-MM-DD
    return_date: str = ""  # YYYY-MM-DD
    repayment_terms: str = ""

    @property
    def version(self) -> str:
        return "1.0.0"
