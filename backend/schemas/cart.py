from pydantic import BaseModel, Field


class CartItemRequest(BaseModel):
	book_id: int
	quantity: int = Field(..., ge=0)