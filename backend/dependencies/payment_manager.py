from pathlib import Path
from fastapi import Request

from ..src.payment_manager import PaymentManager

PAYMENTS = Path(__file__).parent.parent / "data" / "payments.csv"


def load_payment_manager() -> PaymentManager:
    payment_manager = PaymentManager()
    payment_manager.load_csv(PAYMENTS)
    return payment_manager


def get_payment_manager(request: Request) -> PaymentManager:
    return request.app.state.payment_manager