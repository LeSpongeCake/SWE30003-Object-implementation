from .order import Order
from .payment_manager import PaymentManager
from .repository import Repository
from .singleton import Singleton


class OrderManager(metaclass=Singleton):

    def __init__(self, repo: Repository):
        self.repo = repo

    def add_order(self, order: Order):
        self.repo.save(order)

    def remove_order(self, order_id: int):
        self.repo.delete(order_id)

    def get_order_by_id(self, order_id: int) -> Order | None:
        return self.repo.get_by_id(order_id)

    def get_orders(self) -> list[Order]:
        return self.repo.get_all()

    def get_orders_by_account_id(self, account_id: int) -> list[Order]:
        return [o for o in self.repo.get_all() if o.account_id == account_id]

    def generate_order_id(self) -> int:
        all_ids = [o.order_id for o in self.repo.get_all()]
        return max(all_ids, default=0) + 1

    def pay_order(
        self,
        order_id: int,
        full_name: str,
        email: str,
        address: str,
        shipping_method: str,
        payment_method: str,
        payment_manager: PaymentManager,
    ) -> str:
        order = self.repo.get_by_id(order_id)
        if order is None:
            raise ValueError("Order not found.")
        if order.status != "PENDING":
            raise ValueError("Only pending orders can be paid.")

        msg = payment_manager.pay(
            order_id, full_name, email, address, shipping_method, payment_method
        )
        order.set_status("PAID")
        self.repo.save(order)
        return msg

    def cancel_order(self, order_id: int) -> Order:
        order = self.repo.get_by_id(order_id)
        if order is None:
            raise ValueError("Order not found.")
        if order.status == "CANCELLED":
            raise ValueError("Order is already cancelled.")
        if order.status == "PAID":
            raise ValueError("Unable to cancel a paid order.")

        order.set_status("CANCELLED")
        self.repo.save(order)
        return order