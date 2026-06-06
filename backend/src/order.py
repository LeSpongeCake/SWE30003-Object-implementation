import json
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

    def to_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "account_id": self.account_id,
            "items": json.dumps(self.items),
            "total_price": self.total_price,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Order":
        return cls(
            order_id=int(data["order_id"]),
            account_id=int(data["account_id"]),
            items={int(k): int(v) for k, v in json.loads(data["items"]).items()},
            total_price=float(data["total_price"]),
            status=data["status"],
        )
