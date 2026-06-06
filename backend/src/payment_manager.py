from .payment import Payment
from .payment_method import PaymentMethod, CardPayment, ApplePay, GooglePay
from .repository import Repository


class PaymentManager:

    def __init__(self, repo: Repository):
        self.repo = repo
        self.payment_methods: dict[str, PaymentMethod] = {
            "card": CardPayment(),
            "apple": ApplePay(),
            "google": GooglePay(),
        }

    def get_payments(self) -> list[Payment]:
        return self.repo.get_all()

    def get_payment_by_id(self, payment_id: int) -> Payment | None:
        return self.repo.get_by_id(payment_id)

    def get_payment_by_order_id(self, order_id: int) -> Payment | None:
        return next(
            (p for p in self.repo.get_all() if p.order_id == order_id),
            None
        )

    def pay(
        self,
        order_id: int,
        full_name: str,
        email: str,
        address: str,
        shipping_method: str,
        payment_method: str,
    ) -> str:
        method = self.payment_methods.get(payment_method)
        if method is None:
            return "Not a valid payment method."

        msg = method.pay()
        payment = Payment(
            id=self._generate_id(),
            order_id=order_id,
            full_name=full_name,
            email=email,
            address=address,
            shipping_method=shipping_method,
            payment_method=payment_method,
        )
        self.repo.save(payment)
        return msg

    def remove_payment(self, payment_id: int):
        self.repo.delete(payment_id)

    def _generate_id(self) -> int:
        all_ids = [p.id for p in self.repo.get_all()]
        return max(all_ids, default=0) + 1