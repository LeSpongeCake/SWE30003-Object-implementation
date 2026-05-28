from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException, Query

from ..schemas.book import BookResponse
from ..dependencies.catalogue import get_catalogue

# Tags for documentation
router = APIRouter(tags=["books"])  


@router.get(
    "/search",
    response_model=list[BookResponse],
    summary="Search for books",
    description="Search books using a query."
)
def search(
    q: str,
    sort_by: str = Query("title"),
    order: str = Query("asc"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    catalogue = Depends(get_catalogue),
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
            offset=offset
        )
    ]
    

@router.get(
    "/",
    response_model=list[BookResponse],
    summary="Get all books",
    description="Retrieve all books available in the catalogue."
)
def get_books(catalogue = Depends(get_catalogue)):
    return [
        BookResponse(**asdict(book))
        for book in catalogue.get_books()
    ]


@router.get(
    "/{book_id}",
    response_model=BookResponse,
    summary="Get a book by its ID",
    description="Retrieve a single book from the catalogue by its ID."
)
def get_book(book_id: int, catalogue = Depends(get_catalogue)):
    book = catalogue.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    return BookResponse(
        **book.__dict__
    )