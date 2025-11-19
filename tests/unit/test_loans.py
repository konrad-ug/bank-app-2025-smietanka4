from src.personal_account import PersonalAccount
import pytest

class TestAccount:

    @pytest.fixture
    def account(self):
        account = PersonalAccount("John", "Doe", "12345678911")
        return account

    def test_loan_approved_three_incoming_transfers(self, account):
        account.history = [1000,1000,500]

        result = account.submit_for_loan(3000)

        assert result

        assert account.balance == 3000.0

    def test_loan_approved_summed_five_transactions(self, account):
        account.history = [1000,5000,-500,-1000,2500]

        result = account.submit_for_loan(3000)

        assert result

        assert account.balance == 3000.0

    @pytest.mark.parametrize("transactions, loan_amount, expected_balance", [
        # 1: Ostatnie 3 przelewy nie są przychodzące
        ([1000, -500, 1000], 3000, 1500.0),

        # 2: Niewystarczająca liczba transakcji
        ([1000,1000,1000,-1000], 1000, 2000.0),

        # 3: Suma 5 transakcji mniejsza niż kwota pożyczki
        ([1000,1000,1000,-1000,-1000], 2000, 1000.0),

        # 4: Puste konto, brak historii
        ([], 1000, 0.0),

        # 5: Suma 5 transakcji dokładnie równa kwocie pożyczki
        ([1000,1000,1000,-1000,3000], 5000, 5000.0)
    ])

    def test_loan_declined_scenarios(self, account, transactions, loan_amount, expected_balance):
        for amount in transactions:
            if amount > 0:
                account.incoming_transfer(amount)
            else:
                account.outgoing_transfer(abs(amount))

        assert account.balance == sum(transactions)
        
        result = account.submit_for_loan(loan_amount)

        assert not result
        assert account.balance == expected_balance

    # def test_loan_declined_last_three_transactions_werent_incoming_transfers(self, account):
    #     account.incoming_transfer(1000)
    #     account.outgoing_transfer(500)
    #     account.incoming_transfer(1000)

    #     result = account.submit_for_loan(3000)
    #     assert not result

    #     assert account.balance == 1500.0

    # def test_loan_declined_unsufficient_amount_of_transactions(self, account):
    #     account.incoming_transfer(1000)
    #     account.incoming_transfer(1000)
    #     account.incoming_transfer(1000)
    #     account.outgoing_transfer(1000)

    #     result = account.submit_for_loan(1000)
    #     assert not result

    #     assert account.balance == 2000.0


    # def test_loan_declined_sufficient_amount_of_transactions_but_sum_is_less_than_loan(self, account):
    #     account.incoming_transfer(1000)
    #     account.incoming_transfer(1000)
    #     account.incoming_transfer(1000)
    #     account.outgoing_transfer(1000)
    #     account.outgoing_transfer(1000)

    #     result = account.submit_for_loan(2000)
    #     assert not result

    #     assert account.balance == 1000.0