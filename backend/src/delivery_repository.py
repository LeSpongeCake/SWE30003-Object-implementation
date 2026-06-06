from .repository import Repository
from .delivery import Delivery


class DeliveryRepository(Repository):
    _fieldnames = ["delivery_id", "order_id", "account_id", "status"]

    def _row_to_item(self, row: dict) -> Delivery:
        return Delivery.from_dict(row)

    def _item_to_row(self, delivery: Delivery) -> dict:
        return delivery.to_dict()

    def _get_id(self, delivery: Delivery) -> int:
        return delivery.delivery_id