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
	return account_manager


def get_account_manager(request: Request) -> AccountManager:
	return request.app.state.account_manager