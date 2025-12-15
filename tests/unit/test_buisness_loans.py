from src.company_account import CompanyAccount
import pytest

class TestAccount:

    @pytest.fixture
    def account(self, mocker):
        mock = mocker.patch('src.company_account.requests.get')
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {
            "result": {
                "subject": {
                    "statusVat": "Czynny"
                }
            }
        }

        account = CompanyAccount("UG", "1234567890")
        return account

    @pytest.mark.parametrize("transactions, loan_amount, expected_balance, expected_result", [
        # 1. Saldo na rachunku NIE jest 2 razy większe niż kwota zaciąganego kredytu, i jest opłata ZUS
        ([5000,5000,-1775], 5000, 8225.0, False),

        # 2. Saldo na rachunku JEST 2 razy większe niż kwota zaciąganego kredytu, ale brakuje opłaty ZUS
        ([5000,5000,5000], 5000, 15000.0, False),

        # 3. Saldo na rachunku NIE jest 2 razy większe niż kwota zaciąganego kredytu i brakuje opłaty ZUS
        ([5000,5000,5000], 10000.0, 15000.0, False),

        # 4. Puste konto, brak historii
        ([2000, -2000], 2000, 0.0, False),

        # 5.
        ([5000,5000,-1775, 75], 4150, 12450.0, True)

        
    ])

    def test_loan_scenarios(self, account, transactions, loan_amount, expected_balance, expected_result):
        for amount in transactions:
            if amount > 0:
                account.incoming_transfer(amount)
            else:
                account.outgoing_transfer(abs(amount))
        
        assert account.balance == sum(transactions)

        result = account.take_loan(loan_amount)

        if result == False:
            assert not result
        else:
            assert result
            
        assert account.balance == expected_balance