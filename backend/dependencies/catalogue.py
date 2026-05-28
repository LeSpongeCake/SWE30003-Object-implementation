from pathlib import Path
from datetime import datetime

import pandas as pd
from fastapi import Request

from ..src.book import Book
from ..src.catalogue import Catalogue

BOOKS = Path(__file__).parent.parent / "data" / "books.csv"


def load_catalogue():
    catalogue = Catalogue()
    df = pd.read_csv(BOOKS)
    books = [
        Book(
            id=row["id"],
            title=row["title"],
            authors=row["authors"].split(","),
            genre=row["genre"],
            isbn=str(row["isbn"]),
            num_pages=row["num_pages"],
            publisher=row["publisher"],
            publication_date=datetime.strptime(row["publication_date"], "%Y-%m-%d").date(),
            price=row["price"],
        )
        for _, row in df.iterrows()
    ]
    for book in books:
        catalogue.add_book(book)
    return catalogue


def get_catalogue(request: Request) -> Catalogue:
    return request.app.state.catalogue