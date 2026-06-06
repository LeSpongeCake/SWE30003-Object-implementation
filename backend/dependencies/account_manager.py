from pathlib import Path

import pandas as pd
from fastapi import Request

from ..src.account import CustomerAccount, AdminAccount
from ..src.account_manager import AccountManager

ACCOUNTS = Path(__file__).parent.parent / "data" / "accounts.csv"


def load_account_manager():
	account_manager = AccountManager()
	df = pd.read_csv(ACCOUNTS)
	accounts = [
	{
		"id": int(row["id"]),
		"name": row["name"],
		"username": row["username"],
		"password": row["password"],
		"role": row["role"],
	}
	for _, row in df.iterrows()
	]
		
	for account in accounts:
		if account["role"] == "customer":
			cls = CustomerAccount
		elif account["role"] == "admin":
			cls = AdminAccount
		else:
			raise ValueError(f"Unknown role: {account['role']}")
		new_account = cls(account["id"], account["name"], account["username"], account["password"])
		account_manager.add_account(new_account)
		
	# Ensure default users exist
	import hashlib
	admin_hash = hashlib.sha256(b'admin123').hexdigest()
	user_hash = hashlib.sha256(b'user123').hexdigest()

	if not account_manager.get_account_by_username("admin@bookshelf.local"):
		new_id = max((int(acc.id) for acc in account_manager.get_accounts().values()), default=0) + 1
		account_manager.add_account(AdminAccount(new_id, "Admin User", "admin@bookshelf.local", admin_hash))
		
	if not account_manager.get_account_by_username("ava@bookshelf.local"):
		new_id = max((int(acc.id) for acc in account_manager.get_accounts().values()), default=0) + 1
		account_manager.add_account(CustomerAccount(new_id, "Ava Reader", "ava@bookshelf.local", user_hash))
		
	return account_manager


def get_account_manager(request: Request) -> AccountManager:
	return request.app.state.account_manager