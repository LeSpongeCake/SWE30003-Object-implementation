from pydantic import BaseModel, EmailStr


class PaymentRequest(BaseModel):
    full_name: str
    email: EmailStr
    address: str
    shipping_method: str
    payment_method: str    
    

class PaymentResponse(BaseModel):
    id: int
    order_id: int
    full_name: str
    email: EmailStr
    address: str
    shipping_method: str
    payment_method: str    