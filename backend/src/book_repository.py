from .book import Book
from .repository import Repository


class BookRepository(Repository):
    _fieldnames = ["id", "title", "authors", "genre", "isbn",
                   "num_pages", "publisher", "publication_date", "price"]

    def _row_to_item(self, row: dict) -> Book:
        return Book.from_dict(row)

    def _item_to_row(self, book: Book) -> dict:
        return book.to_dict()

    def _get_id(self, book: Book) -> int:
        return book.id