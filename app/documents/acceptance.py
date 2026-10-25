"""Document #8: Acceptance act (Акт приёма-передачи)."""

from dataclasses import dataclass


@dataclass
class AcceptanceData:
    """Form data for the acceptance act document."""

    # Parties
    transferor_name: str = ""
    transferor_address: str = ""
    transferee_name: str = ""
    transferee_address: str = ""

    # Transfer details
    transfer_date: str = ""  # YYYY-MM-DD
    item_description: str = ""
    item_condition: str = ""
    defects: str = ""
    reference_contract: str = ""

    @property
    def version(self) -> str:
        return "1.0.0"
