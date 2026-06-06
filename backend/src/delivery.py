from dataclasses import dataclass

@dataclass
class Delivery:
    delivery_id: int
    order_id: int
    account_id: int
    status: str = "PREPARING"

    def set_status(self, new_status: str):
        self.status = new_status

    def to_dict(self) -> dict:
        return {
            "delivery_id": self.delivery_id,
            "order_id": self.order_id,
            "account_id": self.account_id,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Delivery":
        return cls(
            delivery_id=int(data["delivery_id"]),
            order_id=int(data["order_id"]),
            account_id=int(data["account_id"]),
            status=data["status"],
        )