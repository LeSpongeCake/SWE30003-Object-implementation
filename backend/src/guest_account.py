from .account import Account

class GuestAccount(Account):
    def __init__(
        self, 
        account_id: int, 
    ):
        super().__init__(account_id, "Guest")

    def get_role(self):
        return "Guest"
