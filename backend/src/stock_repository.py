import csv


class StockRepository:
    def __init__(self, path: str):
        self.path = path
        self._stock: dict[int, int] = {}
        self._load()

    def _load(self):
        try:
            with open(self.path, "r", newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    self._stock[int(row["id"])] = int(row["quantity"])
        except FileNotFoundError:
            self._save()

    def _save(self):
        with open(self.path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "quantity"])
            writer.writeheader()
            for book_id, qty in self._stock.items():
                writer.writerow({"id": book_id, "quantity": qty})

    def get(self, book_id: int) -> int | None:
        return self._stock.get(book_id)

    def get_all(self) -> dict[int, int]:
        return dict(self._stock)

    def set(self, book_id: int, qty: int):
        self._stock[book_id] = qty
        self._save()

    def delete(self, book_id: int):
        self._stock.pop(book_id, None)
        self._save()