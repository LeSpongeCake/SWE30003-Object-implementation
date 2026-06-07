from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException, Query, status

from ..dependencies.catalogue import get_catalogue
from ..dependencies.stock_manager import get_stock_manager
from ..schemas.book import BookResponse, CreateBookRequest
from ..src.book import Book
from ..src.catalogue import Catalogue

router = APIRouter(tags=["books"])


@router.get(
    "/search",
    response_model=list[BookResponse],
    summary="Search for books",
    description="Search books using a query.",
)
def search(
    q: str,
    sort_by: str = Query("title"),
    order: str = Query("asc"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    catalogue: Catalogue = Depends(get_catalogue),
):
    reverse = order != "asc"
    valid_sort_fields = {"title", "price", "date"}
    if sort_by not in valid_sort_fields:
        sort_by = None

    return [
        BookResponse(**asdict(book))
        for book in catalogue.search(
            query=q,
            sort_by=sort_by,
            reverse=reverse,
            limit=limit,
            offset=offset,
        )
    ]


@router.get(
    "/",
    response_model=list[BookResponse],
    summary="Get all books",
    description="Retrieve all books available in the catalogue.",
)
def get_books(catalogue: Catalogue = Depends(get_catalogue)):
    return [BookResponse(**asdict(book)) for book in catalogue.get_books()]


@router.get(
    "/with-stock",
    summary="Get all books with current stock",
    description="Retrieve all books with an added `stock` field from inventory.",
)
def get_books_with_stock(
    catalogue: Catalogue = Depends(get_catalogue),
    stock_manager=Depends(get_stock_manager),
):
    stock_map = stock_manager.get_stock()
    result = []
    for book in catalogue.get_books():
        data = asdict(book)
        # normalize for client expectations
        data["author"] = data.get("authors", [None])[0] if data.get("authors") else None
        pub_date = data.get("publication_date")
        try:
            data["year"] = int(str(pub_date).split("-")[0]) if pub_date else None
        except Exception:
            data["year"] = None
        data["genreKey"] = data.get("genre")
        data["genreLabel"] = data.get("genre")
        data["tag"] = data.get("tag", "")
        data["summary"] = data.get("summary", "")
        data["stock"] = stock_map.get(data.get("id"), 0)
        result.append(data)
    return result


@router.get(
    "/genres",
    summary="Get available genres",
    description="Return a list of genres (key, label and count) present in the catalogue.",
)
def get_genres(catalogue: Catalogue = Depends(get_catalogue)):
    books = catalogue.get_books()
    counts: dict[str, int] = {}
    for book in books:
        key = getattr(book, "genre", "") or ""
        counts[key] = counts.get(key, 0) + 1

    result = []
    for key, cnt in sorted(counts.items(), key=lambda kv: kv[0]):
        result.append({"key": key, "label": key, "count": cnt})
    return result


@router.get(
    "/{book_id}",
    response_model=BookResponse,
    summary="Get a book by its ID",
    description="Retrieve a single book from the catalogue by its ID.",
)
def get_book(book_id: int, catalogue: Catalogue = Depends(get_catalogue)):
    book = catalogue.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found.")
    return BookResponse(**asdict(book))


@router.post(
    "/add",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a book to the catalogue",
    description="Create and add a new book to the catalogue, returns the newly created book.",
)
def add_book(request: CreateBookRequest, catalogue=Depends(get_catalogue)):
    new_id = max((book.id for book in catalogue.get_books()), default=0) + 1
    book = Book(id=new_id, **request.model_dump())
    catalogue.add_book(book)
    return BookResponse(**asdict(book))