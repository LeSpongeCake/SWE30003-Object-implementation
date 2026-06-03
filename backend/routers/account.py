import hashlib
from dataclasses import asdict

from fastapi import APIRouter, Depends, status

from ..dependencies.account_manager import get_account_manager
from ..schemas.account import LoginRequest, CreateAccountRequest
from ..src.account import CustomerAccount

router = APIRouter(tags=["account"])


@router.get(
	"/me",
	summary="Get current active session",
	description="Returns the session ID and the account associated with the session."
)
def get_active_session(account_manager = Depends(get_account_manager)):
	session = account_manager.get_current_session()
	account = session.get_account()
	return {
		"session_id": session.session_id,
		"account_id": account.id,
		"name": account.name,
		"username": account.username,
		"role": account.get_role(),
		"cart_items": session.cart.get_items()
	}

@router.post(
	"/login",
	summary="Log in",
	description="Attempt a login with the provided credentials."
)
def login(request: LoginRequest, account_manager = Depends(get_account_manager)):
	username, password = request.username, request.password
	session = account_manager.login(username=username, password=password)
	if session is not None:
		return {
			"session_id": session.session_id,
			"account_id": session.account.id,
			"name": session.account.name,
			"username": session.account.username
		}
	return {"error": "Invaild credentials"}

@router.post(
	"/logout",
	summary="Log out",
	description="Log out / Switch to a guest session."
)
def logout(account_manager = Depends(get_account_manager)):
	account_manager.logout()
	session = account_manager.get_current_session()
	return {
		"session_id": session.session_id
	}

@router.post(
	"/create",
	status_code=status.HTTP_201_CREATED,
	summary="Create a new account",
	description="Create a new Customer Account and record the account to the database"
)
def create_account(
	request: CreateAccountRequest, 
	account_manager = Depends(get_account_manager)
):
	new_id = max((
		id for id in account_manager.get_accounts()), 
		default=0
	) + 1
	request.password = hashlib.sha256(request.password.encode()).hexdigest()
	account = CustomerAccount(new_id, **request.model_dump())
	account_manager.add_account(account)
	return {
		"message": "Account created successfully."
	}