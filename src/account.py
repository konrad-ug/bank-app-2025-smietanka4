from datetime import date
from lib.smtp_client import SMTPClient

class Account:
    def __init__(self):
        self.balance = 0.0
        self.history = []

    def outgoing_transfer(self, amount: float ):
        if amount <= 0:
            return self.balance
        if amount > self.balance:
            return self.balance
        self.balance -= amount
        self.history.append(-amount)
        return self.balance


    def incoming_transfer(self, amount: float ):
        if amount <= 0:
            return self.balance
        self.balance += amount
        self.history.append(amount)
        return self.balance

    def outgoing_express_transfer(self, amount: float):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount + self.outgoing_express_transfer_fee
            self.history.append(-amount)
            self.history.append(-self.outgoing_express_transfer_fee)
        return self.balance

    # Druga wersja metody outgoing_express_transfer
    # def outgoing_express_transfer(self, amount: float, fee: float):
    #     if amount <= 0:
    #         return self.balance
        
    #     total = amount + fee

    #     if self.balance >= amount or self.balance + fee >= amount:
    #         self.balance -= total
    #         return self.balance
    #     else:
    #         return self.balance

    def send_history_via_email(self, email_address: str) -> bool:
        today = date.today().strftime("%Y-%m-%d")
        subject = f"Account Transfer History {today}"

        text = f"{self.account_name} account history: {self.history}"

        return SMTPClient.send(subject, text, email_address)


        