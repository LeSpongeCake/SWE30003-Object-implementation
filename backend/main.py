from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .dependencies.account_manager import load_account_manager
from .dependencies.catalogue import load_catalogue
from .dependencies.session_manager import load_session_manager
from .dependencies.stock_manager import load_stock_manager
from .routers import account, books, stock_manager, cart


@asynccontextmanager
async def lifespan(app: FastAPI):
    # This code runs at startup
    app.state.catalogue = load_catalogue()
    app.state.stock_manager = load_stock_manager(catalogue=app.state.catalogue)
    app.state.account_manager = load_account_manager()
    app.state.session_manager = load_session_manager()

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

app = FastAPI(lifespan=lifespan)

# Prefix "/books" is automatically added to all endpoints
app.include_router(account.router, prefix="/account")
app.include_router(books.router, prefix="/books")
app.include_router(cart.router, prefix="/cart")
app.include_router(stock_manager.router, prefix="/stock")

# Serve frontend static files from backend/static (if present) while
# allowing API routes to take precedence.
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    from fastapi import Request
    from fastapi.responses import FileResponse

    API_PREFIXES = ("/books", "/account", "/cart", "/stock", "/docs", "/openapi.json")

    @app.middleware("http")
    async def static_middleware(request: Request, call_next):
        path = request.url.path
        # Let API and docs routes be handled by FastAPI
        if any(path == p or path.startswith(p + "/") for p in API_PREFIXES):
            return await call_next(request)

        # Try to serve an exact static file
        candidate = static_dir / path.lstrip("/")
        if candidate.exists() and candidate.is_file():
            return FileResponse(candidate)

        # Otherwise fall back to index.html (SPA)
        index_file = static_dir / "index.html"
        if index_file.exists():
            return FileResponse(index_file)

        return await call_next(request)