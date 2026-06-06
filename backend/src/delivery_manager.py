from .delivery import Delivery
from .repository import Repository
from .singleton import Singleton


class DeliveryManager(metaclass=Singleton):

    def __init__(self, repo: Repository):
        self.repo = repo

    def _generate_id(self) -> int:
        all_ids = [d.delivery_id for d in self.repo.get_all()]
        return max(all_ids, default=0) + 1

    def create_delivery_for_order(self, order) -> Delivery:
        delivery = Delivery(
            delivery_id=self._generate_id(),
            order_id=order.order_id,
            account_id=order.account_id,
            status="PREPARING",
        )
        self.repo.save(delivery)
        return delivery

    def get_delivery_by_id(self, delivery_id: int) -> Delivery | None:
        return self.repo.get_by_id(delivery_id)

    def get_delivery_by_order_id(self, order_id: int) -> Delivery | None:
        return next(
            (d for d in self.repo.get_all() if d.order_id == order_id),
            None
        )

    def get_deliveries(self) -> list[Delivery]:
        return self.repo.get_all()

    def on_delivering(self, delivery_id: int):
        delivery = self.repo.get_by_id(delivery_id)
        if delivery:
            delivery.set_status("DELIVERING")
            self.repo.save(delivery)

    def on_arrived(self, delivery_id: int):
        delivery = self.repo.get_by_id(delivery_id)
        if delivery:
            delivery.set_status("ARRIVED")
            self.repo.save(delivery)