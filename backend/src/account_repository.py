from .repository import Repository
from .account import Account


class AccountRepository(Repository):
	_fieldnames = ["id", "name", "username", "password", "role"]
	
	# Override as guest accounts aren't persistent
	def save(self, account: Account):
		if not account.is_persistent:
			return
		super().save(account)

	def _row_to_item(self, row: dict) -> Account:
		return Account.from_dict(row)

	def _item_to_row(self, account: Account) -> dict:
		return account.to_dict()

	def _get_id(self, account: Account) -> int:
		return account.id