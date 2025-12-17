import pytest
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount
from lib.smtp_client import SMTPClient
from datetime import date

class TestMails:

    @pytest.fixture
    def mock_smtp(self,mocker):
        return mocker.patch('lib.smtp_client.SMTPClient.send')

    @pytest.fixture(autouse=True)
    def mock_mf_api(self, mocker):
        mock = mocker.patch('src.company_account.requests.get')
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {
            "result": {"subject": {"statusVat": "Czynny"}}
        }
        return mock

    def test_send_email_personal_account_success(self, mock_smtp):
        account = PersonalAccount("John", "Doe", "12345678910")
        account.incoming_transfer(100)
        account.outgoing_transfer(50)
        email = "test@email.com"

        mock_smtp.return_value = True

        result = account.send_history_via_email(email)

        assert result == True
        mock_smtp.assert_called_once()

        args = mock_smtp.call_args[0]

        subject = args[0]
        text = args[1]
        recipient = args[2]

        today = date.today().strftime("%Y-%m-%d")
        assert subject == f"Account Transfer History {today}"
        assert text == "Personal account history: [100, -50]"
        assert recipient == "test@email.com"

    def test_send_email_personal_account_failure(self, mock_smtp):
        email = "test@email.com"
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        
        mock_smtp.return_value = False 

        result = account.send_history_via_email(email)

        assert result == False
        mock_smtp.assert_called_once()
        
        args = mock_smtp.call_args[0]
        assert args[1] == "Personal account history: []"

    def test_send_email_company_account_success(self, mock_smtp):
        account = CompanyAccount("Firma", "1234567890")
        account.incoming_transfer(5000)
        account.outgoing_express_transfer(2000)
        # historia: [5000, -2000, -5]

        email = "test@email.com"

        mock_smtp.return_value = True
        result = account.send_history_via_email(email)

        assert result == True
        mock_smtp.assert_called_once()

        args = mock_smtp.call_args[0]

        subject, text, recipient = args[0], args[1], args[2]

        today = date.today().strftime("%Y-%m-%d")
        assert subject == f"Account Transfer History {today}"
        assert text == "Company account history: [5000, -2000, -5.0]"
        assert recipient == "test@email.com"

    def test_send_email_company_account_failure(self, mock_smtp):
        account = CompanyAccount("Firma", "1234567890")
        email = "test@email.com"

        mock_smtp.return_value = False
        result = account.send_history_via_email(email)

        assert result == False
        mock_smtp.assert_called_once()

        args = mock_smtp.call_args[0]
        assert args[1] == "Company account history: []"





