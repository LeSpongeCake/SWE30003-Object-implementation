from .catalogue import Catalogue

class ShoppingCart():
    def __init__(self):
        # Maps book id to the corresponding item quantity
        self.cart: dict[int, int] = {}

    def add_item(self, book_id: int, qty: int):
        self.cart[book_id] = qty

    def remove_item(self, book_id):
        self.cart.pop(book_id, None)
    
    def get_items(self) -> int:
        """Returns the total number of items in the cart"""
        return len(self.cart)

    def calculate_totals(self, catalogue: Catalogue) -> float:
        books = [self.catalogue.get_book__by_id(book_id) for book_id in self.cart]
        return sum(map(lambda x: x.price, books))