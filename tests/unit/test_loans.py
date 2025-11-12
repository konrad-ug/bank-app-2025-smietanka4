from src.personal_account import PersonalAccount
import pytest

class TestAccount:

    @pytest.fixture
    def account(self):
        account = PersonalAccount("John", "Doe", "12345678911")
        return account

    def test_loan_approved_three_incoming_transfers(self, account):
        account.incoming_transfer(1000)
        account.incoming_transfer(2000)    
        account.incoming_transfer(2500)    

        result = account.submit_for_loan(3000)

        assert result

        assert account.balance == 8500.0

    def test_loan_approved_summed_five_transactions(self, account):
        account.incoming_transfer(1000)
        account.incoming_transfer(5000)
        account.outgoing_transfer(500)
        account.outgoing_transfer(1000)
        account.incoming_transfer(2500)

        result = account.submit_for_loan(3000)

        assert result

        assert account.balance == 10000.0

    def test_loan_declined_last_three_transactions_werent_incoming_transfers(self, account):
        account.incoming_transfer(1000)
        account.outgoing_transfer(500)
        account.incoming_transfer(1000)

        result = account.submit_for_loan(3000)

        assert not result

        assert account.balance == 1500.0

    def test_loan_declined_unsufficient_amount_of_transactions(self, account):
        account.incoming_transfer(1000)
        account.incoming_transfer(1000)
        account.incoming_transfer(1000)
        account.outgoing_transfer(1000)

        result = account.submit_for_loan(1000)
        assert not result

        assert account.balance == 2000.0


    def test_loan_declined_sufficient_amount_of_transactions_but_sum_is_less_than_loan(self, account):
        account.incoming_transfer(1000)
        account.incoming_transfer(1000)
        account.incoming_transfer(1000)
        account.outgoing_transfer(1000)
        account.outgoing_transfer(1000)

        result = account.submit_for_loan(2000)
        assert not result

        assert account.balance == 1000.0