from datetime import date
from dataclasses import dataclass

@dataclass
class Book():
    id: int
    title: str
    authors: list[str]
    genre: str
    isbn: str
    num_pages: int
    publisher: str
    publication_date: date
    price: float