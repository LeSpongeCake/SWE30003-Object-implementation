from dataclasses import dataclass

@dataclass
class Order():
    order_id: int
    account_id: int
    items: dict[int, int]
    total_price: float
    status: str = "PENDING"

    def set_status(self, new_status: str):
        self.status = new_status
