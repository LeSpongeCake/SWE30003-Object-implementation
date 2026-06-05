from pydantic import BaseModel


class DeliveryResponse(BaseModel):
    delivery_id: int
    order_id: int
    account_id: int
    status: str