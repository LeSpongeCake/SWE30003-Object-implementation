from datetime import date

from pydantic import BaseModel

class CreateBookRequest(BaseModel):
    title: str
    authors: list[str]
    genre: str
    isbn: str
    num_pages: int
    publisher: str
    publication_date: date
    price: float
    

class BookResponse(BaseModel):
    id: int
    title: str
    authors: list[str]
    genre: str
    isbn: str
    num_pages: int
    publisher: str
    publication_date: date
    price: float