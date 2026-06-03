from dataclasses import asdict

from fastapi import APIRouter, Depends

from ..dependencies.catalogue import get_catalogue
from ..dependencies.session_manager import get_session_manager
from ..dependencies.stock_manager import get_stock_manager
from ..schemas.cart import CartItemRequest
from ..src.catalogue import Catalogue
from ..src.session_manager import SessionManager
from ..src.stock_manager import StockManager

router = APIRouter(tags=["cart"])


@router.get(
  	path="/",
	summary="Get the current shopping cart",
	description="""
	Return detailed information about the cart, including the account ID, the list of books in the cart, the quantity of each book, the total number of distinct items, and the total price.
	"""
)
def get_items(
	session_manager: SessionManager = Depends(get_session_manager),
	catalogue: Catalogue = Depends(get_catalogue)
):
	session = session_manager.get_current_session()
	cart = session.cart
	items = cart.get_items()

	books = []
	for id, qty in items.items():
		book = {}
		book["book"] = asdict(catalogue.get_book_by_id(id))
		book["quantity"] = qty
		books.append(book)
	
	return {
		"account_id": session.account.id,
		"items": books,
		"total_items": cart.get_number_of_items(),
		"total_price": cart.calculate_totals(catalogue)
	}


@router.get(
	path="/{book_id}",
	summary="Get the quantity the given item in the cart"
)
def get_quantity(
	book_id: int,
	session_manager: SessionManager = Depends(get_session_manager)
):
	cart = session_manager.get_current_session().cart
	return cart.get_item_quantity(book_id)


@router.get(
	path="/total",
	summary="Get cart total"
)
def get_total(session_manager: SessionManager = Depends(get_session_manager)):
	cart = session_manager.get_current_session().cart
	return {
		"total": cart.calculate_totals()
	}


@router.post(
	path="/add",
	summary="Add item to cart",
	description=
	"""
	Add a quantity of the given item to the cart. Return the current quantity of the item if the operation was successful.
	"""
)
def add_item(
	request: CartItemRequest,
	session_manager: SessionManager = Depends(get_session_manager),
	stock_manager: StockManager = Depends(get_stock_manager)
):
	book_id, quantity = request.book_id, request.quantity
	cart = session_manager.get_current_session().cart

	# Check stock first before committing
	stock = stock_manager.get_stock_by_id(book_id)
	if cart.get_item_quantity(book_id) + quantity > stock:
		return {
			"error": "Quantity exceeds available stock."
		}
	cart.add_item(book_id=book_id, qty=quantity)
	return cart.get_item_quantity(book_id)


@router.post(
	path="/remove",
	summary="Remove item from cart",
	description=
	"""
	Remove a quantity of the given item from the shopping cart. Item is complete removed if the quantity to remove exceeds the current quantity in the cart.
	Return the current quantity of the item.
	"""
)
def remove_item(
	request: CartItemRequest,
	session_manager: SessionManager = Depends(get_session_manager),
):
	book_id, quantity = request.book_id, request.quantity
	cart = session_manager.get_current_session().cart
	cart.remove_item(book_id=book_id, qty=quantity)
	return cart.get_item_quantity(book_id)