from book import Book
from collections import defaultdict

class Catalogue:
    def __init__(self):
        # Map each book's ID to its Book object
        self.books: dict[int, Book] = {}

        # Additional indexes for efficient searching
        self.books_by = {
            "author": defaultdict(list),    # Author name to book ids
            "genre":  defaultdict(list),    # Genre name to book ids
            "publisher": defaultdict(list)  # Publisher name to book ids
        } 

        self.isbn: dict[str, int] = {}

    def add_book(self, book: Book):
        """Adds book to the catalogue."""
        self.books[book.id]  = book
        self.isbn[book.isbn] = book.id

        for attribute, nested_dict in self.books_by.items():
            if attribute != "authors":          
                nested_dict[book.get(attribute)].append(book.id)
                continue
            # A book could have multiple authors -> add book_id to all author entries
            for author in book.authors:
                nested_dict[author].append(book.id)

    def remove_book(self, book_id: int) -> Book:
        """Removes book from the catalogue. Returns the removed item, if any."""
        book = self.books.get(book_id)

        if book is None:
            return book

        for attribute, nested_dict in self.books_by.items():
            if attribute != "authors":          
                nested_dict[book.get(attribute)].remove(book.id)
                continue
            for author in book.authors:
                nested_dict[author].remove(book.id)

        del self.books[book.id]
        del self.isbn[book.isbn]

        return book
    
    def get_books(self) -> list[Book]:
        """Returns a list of Book objects."""
        return self.books.values()
    
    def get_book_by_id(self, book_id: int) -> Book:
        """Returns a single book with book_id."""
        return self.books.get(book_id)
    
    def get_books_by_author(self, author: str) -> list[Book]:
        """Returns a list of books written by author."""
        return self._get_books_by("author", author)
    
    def get_books_by_genre(self, genre: str) -> list[Book]:
        """Returns a list of books of genre."""
        return self._get_books_by("genre", genre)
    
    def get_books_by_publisher(self, publisher: str) -> list[Book]:
        """Returns a list of books by genre."""
        return self._get_books_by("publisher", publisher)
    
    def get_book_by_isbn(self, isbn: str) -> Book:
        """Returns a single book by its ISBN."""
        return self.books[self.isbn.get(isbn)]
    
    def sort_books_by_date(self, reverse: bool = False) -> list[Book]:
        """Sort books by date, in ascending order if reverse = False."""
        sorted_ids = sorted(
            self.books.values(),
            key=lambda book: book.publication_date,
            reverse=reverse,
        )
        return [self.books[id] for id in sorted_ids]
    
    def sort_books_by_price(self, reverse: bool = False) -> list[Book]:
        """Sort books by price, in ascending order if reverse = False."""
        sorted_ids = sorted(
            self.books.values(),
            key=lambda book: book.price,
            reverse=reverse,
        )
        return [self.books[id] for id in sorted_ids]
    
    def _get_books_by(self, attr, attr_value):
        nested_dict = self.books_by.get(attr)
        if nested_dict is None:
            return []
        return [self.books.get(id) for id in nested_dict.get(attr_value, [])]