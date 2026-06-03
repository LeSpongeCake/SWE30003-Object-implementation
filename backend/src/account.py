from dataclasses import dataclass


@dataclass
class Account:
    account_id: int
    username: str
        
    def get_role(self):
        return "Account"