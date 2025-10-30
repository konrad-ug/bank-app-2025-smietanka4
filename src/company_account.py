from src.account import Account

class CompanyAccount(Account):
    outgoing_express_transfer_fee = 5.0

    def __init__(self, company_name, nip):
        super().__init__()
        self.company_name = company_name
        self.nip = nip if self.is_nip_valid(nip) else "Invalid"

    def is_nip_valid(self, nip) -> bool:
        if nip and len(nip) == 10:
            return True
        return False
    
    # kompatybilne z drugą wersją metody
    # def outgoing_express_transfer(self, amount):
    #     fee = 1.0
    #     return super().outgoing_express_transfer(amount, fee)
        