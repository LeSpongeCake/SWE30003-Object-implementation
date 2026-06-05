from os import path
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

from ..dependencies.catalogue import get_catalogue
from ..dependencies.order_manager import get_order_manager
from ..dependencies.session_manager import get_session_manager
from ..dependencies.delivery_manager import get_delivery_manager
from ..schemas.order import OrderResponse
from ..src.catalogue import Catalogue
from ..src.order import Order
from ..src.order_manager import OrderManager
from ..src.session_manager import SessionManager
from ..src.delivery_manager import DeliveryManager


ORDERS = Path(__file__).parent.parent / "data" / "orders.csv"
DELIVERIES = Path(__file__).parent.parent / "data" / "deliveries.csv"

router = APIRouter(tags=["orders"])

@router.post(
    path="/",
    summary="Create the order from the current shopping cart",
    response_model=OrderResponse
)
def create_order(
    session_manager: SessionManager = Depends(get_session_manager),
    order_manager: OrderManager = Depends(get_order_manager),
    catalogue: Catalogue = Depends(get_catalogue)
):
    session = session_manager.get_current_session()
    cart = session.cart

    if cart.get_number_of_items() == 0:
        raise HTTPException(status_code=400, detail="Cannot create order from an empty cart.")

    order = Order(
        order_id=order_manager.generate_order_id(),
        account_id=session.account.id,
        items=cart.get_items().copy(),
        total_price=cart.calculate_totals(catalogue),
        status="PENDING"
    )

    order_manager.add_order(order)
    order_manager.export_csv(str(ORDERS))

    return order


@router.get(
    path="/", 
    summary="Get all orders",
    response_model=list[OrderResponse]
)
def get_all_orders(
    order_manager: OrderManager = Depends(get_order_manager)
):
    return list(order_manager.get_orders().values())


@router.get(
    path="/customer/{account_id}",
    summary="Get orders by customer",
    response_model=list[OrderResponse]
)
def get_customer_orders(
    account_id: int,
    order_manager: OrderManager = Depends(get_order_manager)
):
    return order_manager.get_orders_by_account(account_id)


@router.get(
    path="/{order_id}",
    summary="Get order by ID",
    response_model=OrderResponse
)
def get_order_by_id(
    order_id: int,
    order_manager: OrderManager = Depends(get_order_manager)
):
    order = order_manager.get_order_by_id(order_id)

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found.")

    return order


@router.put(
    path="/{order_id}/pay",
    summary="Pay for an order and generate a delivery",
    response_model=OrderResponse
)
def pay_order(
    order_id: int,
    order_manager: OrderManager = Depends(get_order_manager),
    delivery_manager: DeliveryManager = Depends(get_delivery_manager)
):
    try:
        order = order_manager.pay_order(order_id)
        delivery = delivery_manager.create_delivery_for_order(order)

        if order is None:
            raise HTTPException(status_code=404, detail="Order not found.")

        order_manager.export_csv(str(ORDERS))
        delivery_manager.export_csv(str(DELIVERIES))
        return order

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.put(
    path="/{order_id}/cancel",
    summary="Cancel an order",
    response_model=OrderResponse
)
def cancel_order(
    order_id: int,
    order_manager: OrderManager = Depends(get_order_manager)
):
    try:
        order = order_manager.cancel_order(order_id)

        if order is None:
            raise HTTPException(status_code=404, detail="Order not found.")

        order_manager.export_csv(str(ORDERS))
        return order

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))