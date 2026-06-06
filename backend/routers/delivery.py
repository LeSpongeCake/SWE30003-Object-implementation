from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

from ..dependencies.delivery_manager import get_delivery_manager
from ..schemas.delivery import DeliveryResponse
from ..src.delivery_manager import DeliveryManager


DELIVERIES_CSV = Path(__file__).parent.parent / "data" / "delivery.csv"

router = APIRouter(tags=["delivery"])

@router.get(
        path="/",
        summary="Get all deliveries",
        response_model=list[DeliveryResponse]
)
def get_all_deliveries(
    delivery_manager: DeliveryManager = Depends(get_delivery_manager)
):
    return list(delivery_manager.get_deliveries())


@router.get(
    path="/{delivery_id}",
    summary="Get delivery by ID",
    response_model=DeliveryResponse
)
def get_delivery_by_id(
    delivery_id: int,
    delivery_manager: DeliveryManager = Depends(get_delivery_manager)
):
    delivery = delivery_manager.get_delivery_by_id(delivery_id)

    if delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found.")

    return delivery


@router.get(
    path="/order/{order_id}",
    summary="Get delivery by order ID",
    response_model=DeliveryResponse
)
def get_delivery_by_order_id(
    order_id: int,
    delivery_manager: DeliveryManager = Depends(get_delivery_manager)
):
    delivery = delivery_manager.get_delivery_by_order_id(order_id)

    if delivery is None:
        raise HTTPException(
            status_code=404,
            detail="Delivery for this order not found."
        )

    return delivery


@router.put(
    path="/{delivery_id}/delivering",
    summary="Mark delivery as delivering",
    response_model=DeliveryResponse
)
def dispatch_delivery(
    delivery_id: int,
    delivery_manager: DeliveryManager = Depends(get_delivery_manager)
):
    delivery = delivery_manager.get_delivery_by_id(delivery_id)

    if delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found.")

    delivery_manager.on_delivering(delivery_id)
    return delivery


@router.put(
    path="/{delivery_id}/arrived",
    summary="Mark delivery as arrived",
    response_model=DeliveryResponse
)
def complete_delivery(
    delivery_id: int,
    delivery_manager: DeliveryManager = Depends(get_delivery_manager)
):
    delivery = delivery_manager.get_delivery_by_id(delivery_id)

    if delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found.")

    delivery_manager.on_arrived(delivery_id)
    return delivery