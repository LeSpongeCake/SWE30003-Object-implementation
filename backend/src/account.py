import hashlib
from dataclasses import dataclass


@dataclass
class Account:

    def __init__(
        self,
        account_id: int,
        username: str,
        password: str,
    ):
        self.account_id = account_id
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return (
            hashlib.sha256(password.encode()).hexdigest()
            == self.password_hash
        )

    def get_role(self):
        return "Account"
    

class AdminAccount(Account):

    def get_role(self):
        return "Admin"
    
    def edit_permissions(self):
        return True
    

class CustomerAccount(Account):

    def get_role(self):
        return "Customer"
    

class GuestAccount(Account):

    def __init__(self, account_id: int):
        super().__init__(account_id, "Guest")

    def get_role(self):
        return "Guest"