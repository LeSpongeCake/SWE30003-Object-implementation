from datetime import date, datetime
from dataclasses import dataclass, asdict


@dataclass
class Book:
    id: int
    title: str
    authors: list[str]
    genre: str
    isbn: str
    num_pages: int
    publisher: str
    publication_date: date
    price: float

    def __post_init__(self):
        self.price = round(float(self.price), 2)

    def to_dict(self) -> dict:
        row = asdict(self)
        row["authors"] = ",".join(self.authors)
        row["publication_date"] = self.publication_date.isoformat()
        return row

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        return cls(
            id=int(data["id"]),
            title=data["title"],
            authors=data["authors"].split(","),
            genre=data["genre"],
            isbn=str(data["isbn"]),
            num_pages=int(data["num_pages"]),
            publisher=data["publisher"],
            publication_date=datetime.strptime(data["publication_date"], "%Y-%m-%d").date(),
            price=float(data["price"]),
        )