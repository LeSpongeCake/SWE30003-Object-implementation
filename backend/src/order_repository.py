from .repository import Repository
from .order import Order


class OrderRepository(Repository):
    _fieldnames = ["order_id", "account_id", "items", "total_price", "status"]

    def _row_to_item(self, row: dict) -> Order:
        return Order.from_dict(row)

    def _item_to_row(self, order: Order) -> dict:
        return order.to_dict()

    def _get_id(self, order: Order) -> int:
        return order.order_id