import csv

from .account import Account, GuestAccount, CustomerAccount
from .session import Session
from .singleton import Singleton


class AccountManager(metaclass=Singleton):

    def __init__(self):
        self.accounts: dict[int, Account] = {}
        self.accounts_by_username = {}  # Support logging in by username
        self.current_session: Session = Session(GuestAccount())

    def add_account(self, account: Account):
        self.accounts[account.id] = account
        self.accounts_by_username[account.username] = account

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

    def get_account_by_id(self, account_id: int) -> Account | None:
        return self.accounts.get(account_id)
    
    def get_account_by_username(self, username: str) -> Account | None:
        return self.accounts_by_username.get(username)
    
    def get_accounts(self) -> dict[int, Account]:
        return self.accounts

    def get_current_session(self) -> Session:
        return self.current_session
    
    def login(self, username: str, password: str) -> Session | None:
        account = self.get_account_by_username(username)
        
        if account and account.check_password(password):
            self.current_session = Session(account)
            return self.current_session

        return None

    def logout(self):
        self.current_session.logout()
        self.current_session = Session(GuestAccount())

    def remove_account(self, account_id: int):
        self.accounts.pop(account_id, None)