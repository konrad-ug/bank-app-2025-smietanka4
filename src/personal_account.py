from src.account import Account


class PersonalAccount(Account):
    outgoing_express_transfer_fee = 1.0

    def __init__(self, first_name, last_name, pesel, promo_code=None):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        self.promo_code = self.is_promo_code_valid(promo_code)

    def is_pesel_valid(self, pesel):
        if pesel and len(pesel) == 11:
            return True
        return False

    def is_promo_code_valid(self, promo_code):
        if promo_code and len(promo_code) == 8:
            prefix = promo_code[:5]
            if prefix == "PROM_":
                if self.is_elgible_for_promotion(self.pesel):
                    self.balance = 50.0
                    return self.balance
            
    def is_elgible_for_promotion(self, pesel):
        if not self.is_pesel_valid(pesel):
            return False
        year_prefix=int(pesel[:2])
        century_code = int(pesel[2])
        if century_code < 2:
            birth_year = 1900 + year_prefix
        else:
            birth_year = 2000 + year_prefix
        return birth_year > 1960
    
    # kompatybilne z drugą wersją metody
    # def outgoing_express_transfer(self, amount):
    #     fee = 1.0
    #     return super().outgoing_express_transfer(amount, fee)
        

            


