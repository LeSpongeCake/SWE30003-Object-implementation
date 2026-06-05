from pathlib import Path
from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException

from ..dependencies.payment_manager import get_payment_manager
from ..schemas.payment import PaymentResponse
from ..src.payment_manager import PaymentManager


ORDERS = Path(__file__).parent.parent / "data" / "payments.csv"

router = APIRouter(tags=["payments"])


@router.get(
    path="/",
    summary="Get payments",
    response_model=list[PaymentResponse]
)
def get_payments(
    payment_manager: PaymentManager = Depends(get_payment_manager)
):
	return [
		PaymentResponse(**payment.to_dict()) 
		for payment in payment_manager.get_payments()
	]


@router.get(
    path="/{payment_id}",
    summary="Get payment by ID",
    response_model=PaymentResponse
)
def get_payment(
    payment_id: int,
    payment_manager: PaymentManager = Depends(get_payment_manager)
):
	payment = payment_manager.get_payment_by_id(payment_id)
	if payment is None:
		raise HTTPException(status_code=404, detail="Payment not found.")
	return PaymentResponse(**payment.to_dict())


@router.get(
    path="/order/{order_id}",
    summary="Get payment by order ID",
    response_model=PaymentResponse
)
def get_payment_by_order(
    order_id: int,
    payment_manager: PaymentManager = Depends(get_payment_manager)
):
	payment = payment_manager.get_payment_by_order_id(order_id)
	if payment is None:
		raise HTTPException(status_code=404, detail="Payment not found.")
	return PaymentResponse(**payment.to_dict())