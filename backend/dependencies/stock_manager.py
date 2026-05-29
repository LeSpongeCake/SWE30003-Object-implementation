from pathlib import Path

import pandas as pd
from fastapi import Request, Depends

from ..src.stock_manager import StockManager, Catalogue
from .catalogue import get_catalogue

BOOKS = Path(__file__).parent.parent / "data" / "books.csv"
STOCK = Path(__file__).parent.parent / "data" / "stock.csv"


def load_stock_manager(catalogue: Catalogue):
    stock_manager = StockManager(catalogue)
    df = pd.read_csv(STOCK)
    stocks = [{
        "id": int(row["id"]),
        "qty": int(row["quantity"])
    } for _, row in df.iterrows()]

    for stock in stocks:
        stock_manager.set_stock(
            book_id=stock["id"],
            qty=stock["qty"]
        )
    return stock_manager


def get_stock_manager(request: Request) -> StockManager:
    return request.app.state.stock_manager