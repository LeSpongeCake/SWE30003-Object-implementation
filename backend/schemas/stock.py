from pydantic import BaseModel, Field

class StockUpdate(BaseModel):
  book_id: int
  qty: int = Field(..., ge=0)