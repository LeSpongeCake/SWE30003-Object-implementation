import csv
import pandas as pd

from .account import Account, CustomerAccount, AdminAccount
from .singleton import Singleton


class AccountManager(metaclass=Singleton):

    def __init__(self):
        self.accounts: dict[int, Account] = {}
        self.accounts_by_username = {}  # Support logging in by username

    def add_account(self, account: Account):
        self.accounts[account.id] = account
        self.accounts_by_username[account.username] = account

    def get_account_by_id(self, account_id: int) -> Account | None:
        return self.accounts.get(account_id)
    
    def get_account_by_username(self, username: str) -> Account | None:
        return self.accounts_by_username.get(username)
    
    def get_accounts(self) -> dict[int, Account]:
        return self.accounts
    
    def export_csv(self, path: str):
        """Export the account database to a CSV file."""
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file, 
                fieldnames=["id", "name", "username", "password", "role"]
            )
            writer.writeheader()

            for id, account in self.accounts.items():
                writer.writerow({
                    "id": id,
                    "name": account.name,
                    "username": account.username,
                    "password": account.password,
                    "role": "customer" if isinstance(account, CustomerAccount) else "admin"
                })
    
    def load_csv(self, path: str):
        df = pd.read_csv(path)
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
            self.add_account(new_account)

    def remove_account(self, account_id: int):
        self.accounts.pop(account_id, None)