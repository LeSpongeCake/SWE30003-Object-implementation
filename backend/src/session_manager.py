from .account import GuestAccount
from .account_manager import AccountManager
from .session import Session
from .singleton import Singleton


class SessionManager(metaclass=Singleton):
	def __init__(self):
		self.current_session: Session = Session(GuestAccount())

	def check_admin_permissions(self) -> bool:
		return self.current_session.account.get_role() == "Admin"

	def get_current_session(self) -> Session:
		return self.current_session
    
	def login(
		self, 
		username: str, 
		password: str,
		account_manager: AccountManager
	) -> Session | None:
		account = account_manager.get_account_by_username(username)

		if account and account.check_password(password):
			self.current_session = Session(account)
			return self.current_session

		return None

	def logout(self):
		self.current_session.logout()
		self.current_session = Session(GuestAccount())
