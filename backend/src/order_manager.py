import csv
import json

from .order import Order
from .singleton import Singleton

class OrderManager(metaclass=Singleton):
    def __init__(self):
        self.orders: dict[int, Order] = {}

    def add_order(self, order: Order):
        self.orders[order.order_id] = order

    def remove_order(self, order_id: int):
        self.orders.pop(order_id, None)

    def get_order_by_id(self, order_id: int) -> Order | None:
        return self.orders.get(order_id)

    def get_orders(self) -> dict[int, Order]:
        return self.orders

    def get_orders_by_account_id(self, account_id: int) -> list[Order]:
        return [
            order 
            for order in self.orders.values()
            if order.account_id == account_id
        ]

    def generate_order_id(self) -> int:
        if not self.orders:
            return 1
        return max(self.orders.keys()) + 1 
    
    def pay_order(self, order_id: int) -> Order:
        order = self.get_order_by_id(order_id)

        if order is None:
            raise ValueError("Order not found.")

        if order.status != "PENDING":
            raise ValueError("Only pending orders can be paid.")

        order.set_status("PAID")
        return order
    
    def cancel_order(self, order_id: int) -> Order:
        order = self.get_order_by_id(order_id)

        if order is None:
            raise ValueError("Order not found.")

        if order.status == "CANCELLED":
            raise ValueError("Order is already cancelled.")

        order.set_status("CANCELLED")
        return order

    def export_csv(self, path: str):
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "order_id",
                    "account_id",
                    "items",
                    "total_price",
                    "status"
                ]
            )
            writer.writeheader()

            for order in self.orders.values():
                writer.writerow({
                    "order_id": order.order_id,
                    "account_id": order.account_id,

                    # Convert items dictionary into JSON string for CSV storage
                    "items": json.dumps(order.items),

                    "total_price": order.total_price,
                    "status": order.status
                })

    def load_csv(self, path: str):
        self.orders.clear()
        
        try:
            with open(path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    order = Order(
                        order_id=int(row["order_id"]),
                        account_id=int(row["account_id"]),

                        # Convert JSON string back into dictionary
                        items={
                            int(k): int(v)
                            for k, v in json.loads(row["items"]).items()
                        },

                        total_price=float(row["total_price"]),
                        status=row["status"]
                    )
                    self.add_order(order)
        except FileNotFoundError:
            self.export_csv(path)