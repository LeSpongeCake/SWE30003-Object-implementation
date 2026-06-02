from .account import Account

class AdminAccount(Account):

    def get_role(self):
        return "Admin"
    
    def edit_permissions(self):
        return True