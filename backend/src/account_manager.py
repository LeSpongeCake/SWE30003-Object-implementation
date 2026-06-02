from .account import Account
from .singleton import Singleton

class AccountManager(metaclass=Singleton):
    def __init__(self):
        self.accounts = {}
        self.current_account = None

    def add_account(self, account):
        self.accounts[account.account.id] = account

    def get_account(self, account_id):
        return self.accounts.get(account_id)
    
    def remove_account(self, account_id):
        self.accounts.pop(account_id, None)

    def login(self, account_id):
        account = self.get_account(account_id)

        if (account):
            self.current_account = self.account

        return account
    
    def logout(self):
        self.current_account = None

    def get_current_account(self):
        return self.current_account
        