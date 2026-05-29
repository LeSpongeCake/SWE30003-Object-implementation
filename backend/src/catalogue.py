import csv
from collections import defaultdict
from dataclasses import asdict

from .book import Book
from .singleton import Singleton

class Catalogue(metaclass=Singleton):
    def __init__(self):
        # Map each book's ID to its Book object
        self.books: dict[int, Book] = {}

        # Additional indexes for efficient searching
        self.indexes: dict[str, dict[str, set[int]]] = defaultdict(lambda: defaultdict(set))

        self.isbn: dict[str, int] = {}

    def add_book(self, book: Book):
        """Adds book to the catalogue."""
        self.books[book.id]  = book
        self.isbn[book.isbn] = book.id

        for attribute, nested_dict in self.indexes.items():
            if attribute != "author":          
                nested_dict[book.__getattribute__(attribute)].add(book.id)
                continue
            # A book could have multiple authors -> add book_id to all author entries
            for author in book.authors:
                nested_dict[author].add(book.id)

    def remove_book(self, book_id: int) -> Book:
        """Removes book from the catalogue. Returns the removed item, if any."""
        book = self.books.get(book_id)

        if book is None:
            return book

        for attribute, nested_dict in self.indexes.items():
            if attribute != "author":          
                nested_dict[book.get(attribute)].remove(book.id)
                continue
            for author in book.authors:
                nested_dict[author].remove(book.id)

        del self.books[book.id]
        del self.isbn[book.isbn]

        return book
    
    def get_books(self) -> list[Book]:
        """Returns a list of Book objects."""
        return list(self.books.values())
    
    def get_book_by_id(self, book_id: int) -> Book:
        """Returns a single book with book_id."""
        return self.books.get(book_id)
    
    def search(
        self,
        query: str,
        sort_by: str = "title",
        reverse: bool = True,
        limit: int = 20,
        offset: int = 0
    ) -> list[Book]:
        """
        Search books by exact matches or scanning titles and authors for partial matches.
        Supports optional sorting and pagination.
        """
        query = query.strip().lower()
        results = set()

        # Exact index matches
        for attr, index in self.indexes.items():
            if query in index:
                results.update(index[query])
        books = [self.books[bid] for bid in results]

        # If no exact matches, scan titles and authors
        if not books:
            books = [
                book for book in self.books.values()
                if query in book.title.lower()
                or any(query in a.lower() for a in book.authors)
            ]

        # Sorting
        if sort_by is not None:
            SORT_FIELDS = {
                "title": lambda b: b.title.lower(),
                "price": lambda b: b.price,
                "date": lambda b: b.publication_date,
            }
        key_func = SORT_FIELDS.get(sort_by)
        # Only sort if valid field provided
        if key_func:
            books = sorted(books, key=key_func, reverse=reverse)

        # Pagination
        return books[offset:offset + limit]
    
    def export_csv(self, path: str):
        """Export the catalogue to a CSV file."""
        books = self.get_books()
        if not books:
            return
        
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=asdict(books[0]).keys()
            )
            writer.writeheader()
            for book in books:
                row = asdict(book)
                # Convert list of authors into a string
                row["authors"] = ",".join(book.authors)
                writer.writerow(row)

    
    def _get_books_by(self, attr: str, attr_value) -> list[Book]:
        nested_dict = self.indexes.get(attr)
        if nested_dict is None:
            return []
        return [self.books[i] for i in nested_dict.get(attr_value, [])]