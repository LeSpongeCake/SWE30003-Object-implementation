from fastapi import FastAPI
from .routers import books

app = FastAPI()

# Prefix "/books" is automatically added to all endpoints
app.include_router(books.router, prefix="/books")