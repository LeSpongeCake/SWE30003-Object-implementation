import csv

from .delivery import Delivery
from .singleton import Singleton


class DeliveryManager(metaclass=Singleton):
    def __init__(self):
        self.deliveries: dict[int, Delivery] = {}

    def generate_delivery_id(self) -> int:
        if not self.deliveries:
            return 1
        return max(self.deliveries.keys()) + 1

    def create_delivery_for_order(self, order):
        delivery = Delivery(
            delivery_id=self.generate_delivery_id(),
            order_id=order.order_id,
            account_id=order.account_id,
            status="PREPARING"
        )
        self.deliveries[delivery.delivery_id] = delivery
        return delivery

    def get_delivery_by_id(self, delivery_id: int):
        return self.deliveries.get(delivery_id)

    def get_delivery_by_order_id(self, order_id: int):
        for delivery in self.deliveries.values():
            if delivery.order_id == order_id:
                return delivery
        return None

    def get_deliveries(self):
        return self.deliveries
    
    def on_delivering(self, delivery_id: int):
        delivery = self.get_delivery_by_id(delivery_id)
        if delivery:
            delivery.set_status("DELIVERING")

    def on_arrived(self, delivery_id: int):
        delivery = self.get_delivery_by_id(delivery_id)
        if delivery:
            delivery.set_status("ARRIVED")

    def export_csv(self, path: str):
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["delivery_id", "order_id", "account_id", "status"]
            )
            writer.writeheader()

            for delivery in self.deliveries.values():
                writer.writerow({
                    "delivery_id": delivery.delivery_id,
                    "order_id": delivery.order_id,
                    "account_id": delivery.account_id,
                    "status": delivery.status
                })

    def load_csv(self, path: str):
        self.deliveries.clear()

        try:
            with open(path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    delivery = Delivery(
                        delivery_id=int(row["delivery_id"]),
                        order_id=int(row["order_id"]),
                        account_id=int(row["account_id"]),
                        status=row["status"]
                    )
                    self.deliveries[delivery.delivery_id] = delivery
        except FileNotFoundError:
            self.export_csv(path)