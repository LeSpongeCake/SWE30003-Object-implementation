from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from .dependencies.account_manager import load_account_manager
from .dependencies.catalogue import load_catalogue
from .dependencies.session_manager import load_session_manager
from .dependencies.stock_manager import load_stock_manager
from .dependencies.order_manager import load_order_manager
from .routers import account, books, stock_manager, cart, orders


@asynccontextmanager
async def lifespan(app: FastAPI):
    # This code runs at startup
    app.state.catalogue = load_catalogue()
    app.state.stock_manager = load_stock_manager(catalogue=app.state.catalogue)
    app.state.account_manager = load_account_manager()
    app.state.session_manager = load_session_manager()
    app.state.order_manager = load_order_manager()

    yield

    #  Re-export modified category at shutdown
    app.state.catalogue.export_csv(
        path=Path(__file__).parent / "data" / "books.csv"
    )
    app.state.stock_manager.export_csv(
        path=Path(__file__).parent / "data" / "stock.csv"
    )
    app.state.account_manager.export_csv(
        path=Path(__file__).parent / "data" / "accounts.csv"
    )
    app.state.order_manager.export_csv(
        path=Path(__file__).parent / "data" / "orders.csv"
    )

app = FastAPI(lifespan=lifespan)

# Prefix "/books" is automatically added to all endpoints
app.include_router(account.router, prefix="/account")
app.include_router(books.router, prefix="/books")
app.include_router(cart.router, prefix="/cart")
app.include_router(stock_manager.router, prefix="/stock")
app.include_router(orders.router, prefix="/orders")