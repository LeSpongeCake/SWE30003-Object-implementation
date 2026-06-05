from pathlib import Path

import pandas as pd
from fastapi import Request

from ..src.account import CustomerAccount, AdminAccount
from ..src.account_manager import AccountManager

ACCOUNTS = Path(__file__).parent.parent / "data" / "accounts.csv"


def load_account_manager():
	account_manager = AccountManager()
	account_manager.load_csv(path=ACCOUNTS)
	return account_manager


def get_account_manager(request: Request) -> AccountManager:
	return request.app.state.account_manager