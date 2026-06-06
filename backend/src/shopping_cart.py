from .catalogue import Catalogue
from .book import Book


class ShoppingCart:
    def __init__(self):
        # book_id -> quantity
        self.cart: dict[int, int] = {}

    def add_item(self, book_id: int, qty: int = 1):
        # Default starts at 0, then increases
        if book_id not in self.cart:
            self.cart[book_id] = 0
        self.cart[book_id] += qty

    def remove_item(self, book_id: int, qty: int = 1):
        book = self.cart.get(book_id)
        if book is None:
            return
        self.cart[book_id] -= qty
        if self.cart[book_id] <= 0:
            self.cart.pop(book_id, None)

    def get_items(self) -> dict[int, int]:
        return self.cart

    def get_item_quantity(self, book_id: int) -> int:
        return self.cart.get(book_id, 0)

    def get_number_of_items(self) -> int:
        """Number of distinct items"""
        return len(self.cart)

    def calculate_totals(self, catalogue: Catalogue) -> float:
        total = 0.0
        for book_id, qty in self.cart.items():
            book = catalogue.get_book_by_id(book_id)
            if book:
                total += book.price * qty
        return total