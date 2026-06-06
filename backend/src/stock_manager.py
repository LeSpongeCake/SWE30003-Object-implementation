from .catalogue import Catalogue
from .singleton import Singleton
from .stock_repository import StockRepository


class StockManager(metaclass=Singleton):

    def __init__(self, repo: StockRepository, catalogue: Catalogue):
        self.repo = repo
        self.catalogue = catalogue

    def get_stock(self) -> dict[int, int]:
        return self.repo.get_all()

    def get_stock_by_id(self, book_id: int) -> int:
        qty = self.repo.get(book_id)
        return qty if qty is not None else -1

    def add_stock(self, book_id: int, qty: int) -> bool:
        if not self._book_exists(book_id):
            return False
        if qty < 0:
            raise ValueError("Quantity must be greater than 0.")
        self.repo.set(book_id, (self.repo.get(book_id) or 0) + qty)
        return True

    def set_stock(self, book_id: int, qty: int) -> bool:
        if not self._book_exists(book_id):
            return False
        if qty < 0:
            raise ValueError("Quantity must be greater than 0.")
        self.repo.set(book_id, qty)
        return True

    def remove_stock(self, book_id: int, qty: int) -> bool:
        if not self._book_exists(book_id):
            return False
        if qty < 0:
            raise ValueError("Quantity must be greater than 0.")
        current = self.repo.get(book_id) or 0
        if qty > current:
            raise ValueError("Quantity exceeds available stock.")
        self.repo.set(book_id, current - qty)
        return True

    def _book_exists(self, book_id: int) -> bool:
        return self.catalogue.get_book_by_id(book_id) is not None