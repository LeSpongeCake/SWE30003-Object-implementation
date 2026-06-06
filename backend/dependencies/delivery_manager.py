from pathlib import Path
from fastapi import Request

from ..src.delivery_manager import DeliveryManager
from ..src.delivery_repository import DeliveryRepository

DELIVERIES = Path(__file__).parent.parent / "data" / "deliveries.csv"


def load_delivery_manager() -> DeliveryManager:
    manager = DeliveryManager(DeliveryRepository(DELIVERIES))
    return manager

def get_delivery_manager(request: Request) -> DeliveryManager:
    return request.app.state.delivery_manager