from fastapi import APIRouter, Depends, HTTPException

from ..dependencies.stock_manager import get_stock_manager
from ..schemas.stock import StockUpdate

# Tags for documentation
router = APIRouter(tags=["stock"])  

@router.get(
    "/",
    summary="Show current inventory",
    description="Return book IDs mapped to its current stock level.")
def get_stock(stock_manager = Depends(get_stock_manager)):
    return stock_manager.get_stock()

@router.post(
	"/add",
	summary="Add stock to inventory",
	description="Add qty to the stock for the given book_id.")
def add_stock(
	  request: StockUpdate,
      stock_manager = Depends(get_stock_manager)):
    book_id, qty = (request.book_id, request.qty)
    if not stock_manager.add_stock(book_id, qty):
         raise HTTPException(
            status_code=404,
            detail=f"Book with id {book_id} not found."
        )
    return {
        "message": "Stock updated successfully."
    }


@router.post(
	"/set",
	summary="Set a book's stock level",
	description="Set the stock for the given book_id to a certain value.")
def set_stock(
	  request: StockUpdate,
      stock_manager = Depends(get_stock_manager)):
    book_id, qty = (request.book_id, request.qty)
    if not stock_manager.set_stock(book_id, qty):
         raise HTTPException(
            status_code=404,
            detail=f"Book with id {book_id} not found."
        )
    return {
        "message": "Stock updated successfully."
    }


@router.post(
	"/remove",
	summary="Remove stock from inventory",
	description="Remove qty from the stock for the given book_id.")
def remove_stock(
	  request: StockUpdate,
      stock_manager = Depends(get_stock_manager)):
    book_id, qty = (request.book_id, request.qty)
    try:
        if not stock_manager.remove_stock(book_id, qty):
            raise HTTPException(
                status_code=404,
                detail=f"Book with id {book_id} not found."
            )
    except ValueError:
         raise HTTPException(
            status_code=422,
            detail=
			"Quantity must not exceed available stock.")
    return {
        "message": "Stock updated successfully."
    }