from pytest_mock import MockFixture
import pytest
from src.company_account import CompanyAccount

class TestCompanyAccount:

    @pytest.fixture
    def mock_api(self, mocker: MockFixture):
        # mocker.patch.object(CompanyAccount, "nip_api_validation", return_value=True)
        mock = mocker.patch('src.company_account.requests.get')
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {"result": {"subject": {"statusVat": "Czynny"}}}
        return mock

        
    def test_company_account_creation(self, mock_api):        
        company = CompanyAccount("UG", "1234567890")
        assert company.company_name == "UG"
        assert company.nip == "1234567890"
        assert company.balance == 0.0

    def test_nip_too_short(self):
        company = CompanyAccount("UG", "12345678")
        assert company.nip == 'Invalid'

    def test_nip_too_long(self):
        company = CompanyAccount("UG", "12345678901")
        assert company.nip == "Invalid"

    def test_history_after_operations(self, mock_api):
        company = CompanyAccount("UG", '1234567890')
        company.incoming_transfer(500)
        company.outgoing_express_transfer(300)

        assert company.history == [500,-300, -5]
        assert company.balance == 195.0

    def test_nip_api_validation_returns_false_for_non_active_vat(self,mocker):
        mock = mocker.patch('src.company_account.requests.get')
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {
            "result": {
                "subject": {
                    "statusVat": "Zwolniony"
                }
            }
        }

        with pytest.raises(ValueError, match="Company not registered!"):
            CompanyAccount("Firma Zwolniona", "1234567890")

    def test_nip_api_validation_returns_false_on_api_error(self, mocker):
        mock = mocker.patch('src.company_account.requests.get')
        mock.return_value.status_code = 500

        with pytest.raises(ValueError, match="Company not registered!"):
            CompanyAccount("Firma Błąd API", "1234567890")
    


        
    