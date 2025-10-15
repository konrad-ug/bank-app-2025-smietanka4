from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe",'12345678911')
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == '12345678911'

    def test_pesel_length_short_pesel(self):
        account = Account("John", "Doe", "123")
        assert account.pesel == 'Invalid' 

    def test_pesel_length_long_pesel(self):
        account = Account("John", "Doe",'123456789123456')
        assert account.pesel == 'Invalid' 

    def test_pesel_length_empty(self):
        account = Account("John", "Doe",'')
        assert account.pesel == 'Invalid'

    def test_discount_correct(self):
        account = Account("John", "Doe", '12345678911', 'PROM_XYZ')
        assert account.balance == 50.0
        

    def test_discount_wrong_format_too_long(self):
        account = Account("John", "Doe", '12345678911', "PROM_XYZABC")
        assert account.balance == 0.0

    def test_discount_wrong_format_too_short(self):
        account = Account("John", "Doe", '12345678911', "PROM_A")        
        assert account.balance == 0.0

    



        
