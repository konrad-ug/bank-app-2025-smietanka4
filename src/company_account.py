from src.account import Account
import requests
import os
from datetime import date

class CompanyAccount(Account):
    outgoing_express_transfer_fee = 5.0

    MF_API_URL = os.environ.get("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl")

    def __init__(self, company_name, nip):
        super().__init__()
        self.company_name = company_name
        if self.is_nip_valid(nip):
            if not self.nip_api_validation(nip):
                raise ValueError("Company not registered!")
            self.nip = nip
        else:
            self.nip = "Invalid"


    def is_nip_valid(self, nip) -> bool:
        if nip and len(nip) == 10:
            return True
        return False

    def take_loan(self, loan_amount) -> bool:
        if (self.balance >= 2*loan_amount):
            if -1775 in self.history:
                self.balance += loan_amount
                return True
        return False

    def nip_api_validation(self, nip: str) -> bool:
        today = date.today().strftime("%Y-%m-d")
        url = f"{self.MF_API_URL}/api/search/nip/{nip}?date={today}"
        print(f"Wysyłam zapytanie do: {url}")

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"Odpowiedź z MF: {data}")

            subject = data.get('result', {}).get('subject', {})
            if subject and subject.get("statusVat") == 'Czynny':
                return True

        return False
    
    # kompatybilne z drugą wersją metody
    # def outgoing_express_transfer(self, amount):
    #     fee = 1.0
    #     return super().outgoing_express_transfer(amount, fee)
        