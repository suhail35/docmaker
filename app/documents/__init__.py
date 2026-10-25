"""Document registry — all 10 legal documents."""

from .invoice import InvoiceData
from .completion import CompletionData
from .service_contract import ServiceContractData
from .receipt import ReceiptData
from .gift import GiftData
from .money_receipt import MoneyReceiptData
from .loan import LoanData
from .acceptance import AcceptanceData
from .pd_consent import PdConsentData
from .fns_application import FnsApplicationData

DOCUMENTS = {
    # Self-employed (НПД)
    "invoice": {
        "name": "Счёт (НПД)",
        "data_class": InvoiceData,
        "template": "documents/invoice.html",
        "category": "self-employed",
    },
    "completion": {
        "name": "Акт выполненных работ",
        "data_class": CompletionData,
        "template": "documents/completion.html",
        "category": "self-employed",
    },
    "service_contract": {
        "name": "Договор возмездного оказания услуг",
        "data_class": ServiceContractData,
        "template": "documents/service_contract.html",
        "category": "self-employed",
    },
    "receipt": {
        "name": "Чек-подтверждение",
        "data_class": ReceiptData,
        "template": "documents/receipt.html",
        "category": "self-employed",
    },
    # Individuals
    "gift": {
        "name": "Договор дарения движимого имущества",
        "data_class": GiftData,
        "template": "documents/gift.html",
        "category": "individual",
    },
    "money_receipt": {
        "name": "Расписка в получении денег",
        "data_class": MoneyReceiptData,
        "template": "documents/money_receipt.html",
        "category": "individual",
    },
    "loan": {
        "name": "Договор займа между физлицами",
        "data_class": LoanData,
        "template": "documents/loan.html",
        "category": "individual",
    },
    "acceptance": {
        "name": "Акт приёма-передачи",
        "data_class": AcceptanceData,
        "template": "documents/acceptance.html",
        "category": "individual",
    },
    "pd_consent": {
        "name": "Согласие на обработку ПДн",
        "data_class": PdConsentData,
        "template": "documents/pd_consent.html",
        "category": "individual",
    },
    "fns_application": {
        "name": "Заявление-пояснение в ФНС",
        "data_class": FnsApplicationData,
        "template": "documents/fns_application.html",
        "category": "individual",
    },
}
