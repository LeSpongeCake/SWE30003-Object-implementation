from .account import Account


class CustomerAccount(Account):
    def __init__(
        self, 
        account_id: int, 
        username: str, 
    ):
        super().__init__(account_id, username)

    def get_role(self):
        return "Customer"