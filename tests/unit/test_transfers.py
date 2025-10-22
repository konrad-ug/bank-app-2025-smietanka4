from src.account import Account

class TestTransfer:
    def test_incoming_transfer(self):
        company = Account()
        company.incoming_transfer(100)
        assert company.balance == 100.0

    def test_incoming_transfer_negative_amount(self):
        company = Account()
        company.incoming_transfer(-50)
        assert company.balance == 0.0

    def test_outgoing_transfer_sufficient_amount(self):
        company = Account()
        company.balance = 100
        company.outgoing_transfer(50)
        assert company.balance == 50

    def test_outgoing_transfer_unsufficient_amount(self):
        company = Account()
        company.outgoing_transfer(50)
        assert company.balance == 0.0