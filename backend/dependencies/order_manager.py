from pathlib import Path
from fastapi import Request

from ..src.order_manager import OrderManager

ORDERS = Path(__file__).parent.parent / "data" / "orders.csv"


def load_order_manager() -> OrderManager:
    manager = OrderManager()
    manager.load_csv(str(ORDERS))
    return manager

def get_order_manager(request: Request) -> OrderManager:
    return request.app.state.order_manager