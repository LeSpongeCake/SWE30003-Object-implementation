from dataclasses import dataclass

@dataclass
class Delivery:
    delivery_id: int
    order_id: int
    account_id: int
    status: str = "PREPARING"

    def set_status(self, new_status: str):
        self.status = new_status