from src.account import Account

class CompanyAccount(Account):
    def __init__(self, company_name, nip):
        self.company_name = company_name
        self.nip = nip if self.is_nip_valid(nip) else "Invalid"
        self.balance = 0.0

    def is_nip_valid(self, nip) -> bool:
        if nip and len(nip) == 10:
            return True
        return False