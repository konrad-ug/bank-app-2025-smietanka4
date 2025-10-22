class Account:
    def __init__(self):
        self.balance = 0.0

    def outgoing_transfer(self, amount: float ):
        if amount <= 0:
            return self.balance
        if amount > self.balance:
            return self.balance
        self.balance -= amount


    def incoming_transfer(self, amount: float ):
        if amount <= 0:
            return self.balance
        self.balance += amount