from catalogue import Catalogue
from collections import defaultdict

class StockManager():
    def __init__(self, catalogue: Catalogue):
        self.catalogue = catalogue
        self.stock: dict[int, int] = defaultdict(0)

    def add_stock(self, book_id: int, qty: int):
        """Adds qty to the stock for the given book_id."""
        self._book_exists(book_id)
        if qty < 0:
            raise ValueError("Quantity must be larger than 0.")
        self.stock[book_id] = self.stock.get(book_id, 0) + qty

    def set_stock(self, book_id: int, qty: int):
        """Sets the stock for the given book_id book_id to qty."""
        self._book_exists(book_id)
        if qty < 0:
            raise ValueError("Quantity must be larger than 0.")
        self.stock[book_id] = qty

    def remove_stock(self, book_id: int, qty: int):
        """Removes a qty of stock for the given book_id.
        Raises an error if the quantity exceeds available stock."""
        self._book_exists(book_id)
        if qty > self.stock.get(book_id):
            raise ValueError("Quantity exceeds available stock.")
        self.stock[book_id] = self.stock.get(book_id) - qty

    def _book_exists(self, book_id: int):
        if book_id not in self.catalogue.books:
            raise ValueError("Book not in catalogue.")