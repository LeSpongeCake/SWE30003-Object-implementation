from pathlib import Path

import pandas as pd
from fastapi import Request

from ..src.account_manager import AccountManager
from ..src.account_repository import AccountRepository

ACCOUNTS = Path(__file__).parent.parent / "data" / "accounts.csv"


def load_account_manager():
	account_manager = AccountManager(AccountRepository(ACCOUNTS))
	return account_manager


def get_account_manager(request: Request) -> AccountManager:
	return request.app.state.account_manager