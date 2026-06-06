from collections import defaultdict

from .book import Book
from .repository import Repository
from .singleton import Singleton


class Catalogue(metaclass=Singleton):

    def __init__(self, repo: Repository):
        self.repo = repo
        self.indexes: dict[str, dict[str, set[int]]] = defaultdict(lambda: defaultdict(set))
        self.isbn: dict[str, int] = {}
        self._build_indexes()

    def _build_indexes(self):
        """Rebuild in-memory indexes from whatever the repo has on load."""
        for book in self.repo.get_all():
            self._index_book(book)

    def _index_book(self, book: Book):
        self.isbn[book.isbn] = book.id
        for attribute, nested_dict in self.indexes.items():
            if attribute != "author":
                nested_dict[getattr(book, attribute)].add(book.id)
            else:
                for author in book.authors:
                    nested_dict[author].add(book.id)

    def _deindex_book(self, book: Book):
        self.isbn.pop(book.isbn, None)
        for attribute, nested_dict in self.indexes.items():
            if attribute != "author":
                nested_dict[getattr(book, attribute)].discard(book.id)
            else:
                for author in book.authors:
                    nested_dict[author].discard(book.id)

    def add_book(self, book: Book):
        self.repo.save(book)
        self._index_book(book)

    def remove_book(self, book_id: int) -> Book | None:
        book = self.repo.get_by_id(book_id)
        if book is None:
            return None
        self._deindex_book(book)
        self.repo.delete(book_id)
        return book

    def get_books(self) -> list[Book]:
        return self.repo.get_all()

    def get_book_by_id(self, book_id: int) -> Book | None:
        return self.repo.get_by_id(book_id)

    def search(
        self,
        query: str,
        sort_by: str = "title",
        reverse: bool = True,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Book]:
        query = query.strip().lower()
        results: set[int] = set()

        for attr, index in self.indexes.items():
            if query in index:
                results.update(index[query])
        books = [self.repo.get_by_id(bid) for bid in results]

        if not books:
            books = [
                book for book in self.repo.get_all()
                if query in book.title.lower()
                or any(query in a.lower() for a in book.authors)
            ]

        SORT_FIELDS = {
            "title": lambda b: b.title.lower(),
            "price": lambda b: b.price,
            "date":  lambda b: b.publication_date,
        }
        key_func = SORT_FIELDS.get(sort_by)
        if key_func:
            books = sorted(books, key=key_func, reverse=reverse)

        return books[offset:offset + limit]

    def _get_books_by(self, attr: str, attr_value) -> list[Book]:
        nested_dict = self.indexes.get(attr)
        if nested_dict is None:
            return []
        return [self.repo.get_by_id(i) for i in nested_dict.get(attr_value, [])]