from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from .routers import books, stock_manager
from .dependencies.catalogue import load_catalogue
from .dependencies.stock_manager import load_stock_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This code runs at startup
    app.state.catalogue = load_catalogue()
    app.state.stock_manager = load_stock_manager(catalogue=app.state.catalogue)

    yield

    #  Re-export modified category at shutdown
    app.state.catalogue.export_csv(
        path=Path(__file__).parent / "data" / "books.csv"
    )
    app.state.stock_manager.export_csv(
        path=Path(__file__).parent / "data" / "stock.csv"
    )

app = FastAPI(lifespan=lifespan)

# Prefix "/books" is automatically added to all endpoints
app.include_router(books.router, prefix="/books")
app.include_router(stock_manager.router, prefix="/stock")
