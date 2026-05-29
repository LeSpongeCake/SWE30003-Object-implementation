import csv
from collections import defaultdict
from dataclasses import asdict

from .singleton import Singleton
from .catalogue import Catalogue

class StockManager(metaclass=Singleton):
    def __init__(self, catalogue: Catalogue):
        self.catalogue = catalogue
        self.stock: dict[int, int] = defaultdict(int)

    def get_stock(self):
        return dict(self.stock)

    def add_stock(self, book_id: int, qty: int):
        """Adds qty to the stock for the given book_id."""
        if not self._book_exists(book_id):
            return False
        if qty < 0:
            raise ValueError("Quantity must be greater than 0.")
        self.stock[book_id] = self.stock.get(book_id, 0) + qty
        return True

    def set_stock(self, book_id: int, qty: int):
        """
        Sets the stock for the given book_id book_id to qty.
        Returns True if operation was successful.
        """
        if not self._book_exists(book_id):
            return False
        if qty < 0:
            raise ValueError("Quantity must be greater than 0.")
        self.stock[book_id] = qty
        return True

    def remove_stock(self, book_id: int, qty: int):
        """
        Removes a qty of stock for the given book_id.
        Raises an error if the quantity exceeds available stock.
        Returns True if operation was successful.
        """
        if not self._book_exists(book_id):
            return False
        if qty < 0:
            raise ValueError("Quantity must be greater than 0.")
        elif qty > self.stock.get(book_id):
            raise ValueError("Quantity exceeds available stock.")
        self.stock[book_id] = self.stock.get(book_id) - qty
        return True
    
    def export_csv(self, path: str):
        """Export the inventory to a CSV file."""
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "quantity"])
            writer.writeheader()

            for book_id, qty in self.stock.items():
                writer.writerow({
                    "id": book_id,
                    "quantity": qty
                })

    def _book_exists(self, book_id: int) -> bool:
        return book_id in self.catalogue.books