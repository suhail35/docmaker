"""Document #5: Gift contract for movable property (Договор дарения движимого имущества)."""

from dataclasses import dataclass


@dataclass
class GiftData:
    """Form data for the gift contract document."""

    # Donor
    donor_name: str = ""
    donor_passport: str = ""
    donor_address: str = ""

    # Donee
    donee_name: str = ""
    donee_passport: str = ""
    donee_address: str = ""
    donee_relationship: str = ""  # e.g. "родственник"

    # Property
    property_description: str = ""
    property_value: float = 0.0
    gift_date: str = ""  # YYYY-MM-DD

    @property
    def version(self) -> str:
        return "1.0.0"
