from contextlib import asynccontextmanager

from fastapi import FastAPI

from .routers import books
from .dependencies.catalogue import load_catalogue

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This code runs at startup
    app.state.catalogue = load_catalogue()

    yield

    # Shutdown code goes here

app = FastAPI(lifespan=lifespan)

# Prefix "/books" is automatically added to all endpoints
app.include_router(books.router, prefix="/books")