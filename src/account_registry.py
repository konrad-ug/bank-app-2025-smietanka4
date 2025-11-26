from src.personal_account import PersonalAccount

class AccountRegistry:
    def __init__(self):
        self.accounts = []

    def add_account(self, account: PersonalAccount):
        self.accounts.append(account)

    def get_account_by_pesel(self, pesel: str):
        for account in self.accounts:
            if account.pesel == pesel:
                return account
        return None

    def get_all_accounts(self):
        return self.accounts
    
    def get_amount_of_accounts(self):
        return len(self.accounts)
    
    def update_account(self, first_name: str, last_name: str, pesel: str):
        account = self.get_account_by_pesel(pesel)
        if account is not None:
            account.first_name = first_name
            account.last_name = last_name
        return None

    def delete_account_by_pesel(self, pesel: str):
        account = self.get_account_by_pesel(pesel)
        if account is not None:
            self.accounts.remove(account)
        return None