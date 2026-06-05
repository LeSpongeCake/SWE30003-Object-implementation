from pathlib import Path
from fastapi import Path, Request

from ..src.order_manager import OrderManager

ORDERS_CSV = Path(__file__).parent.parent / "data" / "orders.csv"


def load_order_manager() -> OrderManager:
    manager = OrderManager()
    manager.load_csv(str(ORDERS_CSV))
    return manager

def get_order_manager(request: Request) -> OrderManager:
    return request.app.state.order_manager