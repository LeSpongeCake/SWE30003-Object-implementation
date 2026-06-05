from pathlib import Path
from datetime import datetime

import pandas as pd
from fastapi import Request

from ..src.book import Book
from ..src.catalogue import Catalogue

BOOKS = Path(__file__).parent.parent / "data" / "books.csv"


def load_catalogue():
    catalogue = Catalogue()
    catalogue.load_csv(path=BOOKS)
    return catalogue


def get_catalogue(request: Request) -> Catalogue:
    return request.app.state.catalogue