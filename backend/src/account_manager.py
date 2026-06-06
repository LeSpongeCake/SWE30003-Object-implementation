from .account import Account
from .repository import Repository
from .singleton import Singleton


class AccountManager(metaclass=Singleton):

    def __init__(self, repo: Repository):
        self.repo = repo

    def add_account(self, account: Account):
        self.repo.save(account)

    def get_account_by_id(self, account_id: int) -> Account | None:
        return self.repo.get_by_id(account_id)

    def get_account_by_username(self, username: str) -> Account | None:
        return next(
            (a for a in self.repo.get_all() if a.username == username),
            None
        )

    def get_accounts(self) -> list[Account]:
        return self.repo.get_all()

    def remove_account(self, account_id: int):
        self.repo.delete(account_id)