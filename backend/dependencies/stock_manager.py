from pathlib import Path

import pandas as pd
from fastapi import Request

from ..src.stock_manager import StockManager, Catalogue
from ..src.stock_repository import StockRepository

STOCK = Path(__file__).parent.parent / "data" / "stock.csv"


def load_stock_manager(catalogue: Catalogue):
    stock_manager = StockManager(StockRepository(STOCK), catalogue)
    return stock_manager


def get_stock_manager(request: Request) -> StockManager:
    return request.app.state.stock_manager