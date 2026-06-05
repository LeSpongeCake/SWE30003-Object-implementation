from pathlib import Path
from fastapi import Request

from ..src.delivery_manager import DeliveryManager

DELIVERIES = Path(__file__).parent.parent / "data" / "deliveries.csv"


def load_delivery_manager() -> DeliveryManager:
    manager = DeliveryManager()
    manager.load_csv(str(DELIVERIES))
    return manager

def get_delivery_manager(request: Request) -> DeliveryManager:
    return request.app.state.delivery_manager