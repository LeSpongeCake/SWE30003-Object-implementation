import hashlib

from fastapi import APIRouter, Depends, status, HTTPException

from ..dependencies.account_manager import get_account_manager
from ..dependencies.session_manager import get_session_manager
from ..schemas.account import LoginRequest, CreateAccountRequest
from ..src.account import CustomerAccount
from ..src.session_manager import SessionManager
from ..src.session_manager import AccountManager

router = APIRouter(tags=["account"])


@router.get(
	"/me",
	summary="Get current active session",
	description="Returns the session ID and the account associated with the session."
)
def get_active_session(session_manager: SessionManager = Depends(get_session_manager)):
	session = session_manager.get_current_session()
	account = session.get_account()
	return {
		"session_id": session.session_id,
		"account_id": account.id,
		"name": account.name,
		"username": account.username,
		"role": account.role,
		"cart_items": session.cart.get_number_of_items()
	}


@router.post(
	"/login",
	summary="Log in",
	description="Attempt a login with the provided credentials."
)
def login(
	request: LoginRequest, 
	session_manager: SessionManager = Depends(get_session_manager),
	account_manager: AccountManager = Depends(get_account_manager)
):
	username, password = request.username, request.password
	session = session_manager.login(
		username=username, 
		password=password,
		account_manager=account_manager
	)
	if session is not None:
		return {
			"session_id": session.session_id,
			"account_id": session.account.id,
			"name": session.account.name,
			"username": session.account.username,
			"role": session.account.role.lower()
		}
	return {"error": "Invalid credentials"}


@router.post(
	"/logout",
	summary="Log out",
	description="Log out / Switch to a guest session."
)
def logout(session_manager: SessionManager = Depends(get_session_manager)):
	session_manager.logout()
	session = session_manager.get_current_session()
	return {
		"session_id": session.session_id
	}

@router.post(
	"/create",
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
	
	# Check if username already exists
	if account_manager.get_account_by_username(account.username):
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail="Email already in use."
		)

	account_manager.add_account(account)
	return {
		"message": "Account created successfully."
	}