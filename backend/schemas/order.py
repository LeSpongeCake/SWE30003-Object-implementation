from pydantic import BaseModel

class OrderResponse(BaseModel):
    order_id: int
    account_id: int
    items: dict[int, int]
    total_price: float
    status: str