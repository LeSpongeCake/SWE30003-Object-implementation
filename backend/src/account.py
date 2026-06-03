import hashlib
from dataclasses import dataclass


@dataclass
class Account:

    def __init__(
        self,
        account_id: int,
        name: str,
        username: str,
        password: str,
    ):
        self.id = account_id
        self.name = name
        self.username = username
        self.password = password

    def check_password(self, password):
        return (
            hashlib.sha256(password.encode()).hexdigest()
            == self.password
        )

    def get_role(self):
        return "Account"
    

class AdminAccount(Account):
    def get_role(self):
        return "Admin"
    

class CustomerAccount(Account):

    def get_role(self):
        return "Customer"
    

class GuestAccount(Account):

    def __init__(self):
        super().__init__(0, "Guest", "", "")

    def get_role(self):
        return "Guest"