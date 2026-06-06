from .repository import Repository
from .payment import Payment


class PaymentRepository(Repository):
    _fieldnames = ["id", "order_id", "full_name", "email",
                   "address", "shipping_method", "payment_method"]

    def _row_to_item(self, row: dict) -> Payment:
        return Payment.from_dict(row)

    def _item_to_row(self, payment: Payment) -> dict:
        return payment.to_dict()

    def _get_id(self, payment: Payment) -> int:
        return payment.id