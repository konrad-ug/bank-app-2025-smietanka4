from src.company_account import CompanyAccount

class TestCompanyAccount:
    def test_company_account_creation(self):
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

    def test_history_after_operations(self):
        company = CompanyAccount("UG", '1234567890')
        company.incoming_transfer(500)
        company.outgoing_express_transfer(300)

        assert company.history == [500,-300, -5]
        assert company.balance == 195.0
    


        
    