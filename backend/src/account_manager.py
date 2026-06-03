from .account import Account, GuestAccount
from .singleton import Singleton


class AccountManager(metaclass=Singleton):

    def __init__(self):
        self.accounts: dict[int, Account] = {}
        self.current_account: Account = None

    def add_account(self, account: Account):
        self.accounts[account.account.id] = account

    def get_account(self, account_id: int) -> Account | None:
        return self.accounts.get(account_id)

    def remove_account(self, account_id: int):
        self.accounts.pop(account_id, None)

    def login(self, account_id: int, password: str) -> Account | None:
        account = self.get_account(account_id)
        if account and account.check_password(password):
            self.current_account = account
        return account

    def logout(self):
        self.current_account = None

    def get_current_account(self) -> Account:
        return self.current_account