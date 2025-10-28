from src.account import Account
from src.company_account import CompanyAccount
from src.personal_account import PersonalAccount

class TestTransfer:
    def test_incoming_transfer(self):
        account = Account()
        account.incoming_transfer(100)
        assert account.balance == 100.0

    def test_incoming_transfer_negative_amount(self):
        account = Account()
        account.incoming_transfer(-50)
        assert account.balance == 0.0

    def test_outgoing_transfer_sufficient_amount(self):
        account = Account()
        account.balance = 100
        account.outgoing_transfer(50)
        assert account.balance == 50

    def test_outgoing_transfer_negative_amount(self):
        account = Account()
        account.balance = 100
        account.outgoing_transfer(-50)
        assert account.balance == 100

    def test_outgoing_transfer_unsufficient_amount(self):
        account = Account()
        account.outgoing_transfer(50)
        assert account.balance == 0.0

    def test_express_outgoing_transfer_personal_account(self):
        account = PersonalAccount("Karol", "Włoczewski", "12345678910")
        account.balance = 50
        account.outgoing_express_transfer(50)
        assert account.balance == -1.0

    def test_express_outgoing_transfer_company_account(self):
        account = CompanyAccount("UG", "1234567890")
        account.balance = 50
        account.outgoing_express_transfer(50)
        assert account.balance == -5.0

    def test_express_outgoing_transfer_personal_account_unsufficient_amount(self):
        account = PersonalAccount("Karol", "Włoczewski", "12345678910")
        account.balance = 50
        account.outgoing_express_transfer(100)
        assert account.balance == 50.0
    
    def test_express_outgoing_transfer_company_account_unsufficient_amount(self):
        account = CompanyAccount("UG", "1234567890")
        account.balance = 50
        account.outgoing_express_transfer(100)
        assert account.balance == 50.0

    def test_express_outgoing_transfer_personal_account_negative_amount(self):
        account = PersonalAccount("Karol", "Włoczewski", "12345678910")
        account.balance = 50
        account.outgoing_express_transfer(-50)
        assert account.balance == 50.0

    def test_express_outgoing_transfer_company_account_negative_amount(self):
        account = CompanyAccount("UG", "1234567890")
        account.balance = 50
        account.outgoing_express_transfer(-50)
        assert account.balance == 50.0

