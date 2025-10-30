from src.personal_account import PersonalAccount

class TestAccount:
    def test_account_creation(self):
        account = PersonalAccount("John", "Doe",'12345678911')
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == '12345678911'

    def test_pesel_length_short_pesel(self):
        account = PersonalAccount("John", "Doe", "123")
        assert account.pesel == 'Invalid' 

    def test_pesel_length_long_pesel(self):
        account = PersonalAccount("John", "Doe",'123456789123456')
        assert account.pesel == 'Invalid' 

    def test_pesel_length_empty(self):
        account = PersonalAccount("John", "Doe",'')
        assert account.pesel == 'Invalid'

    def test_promotion_correct(self):
        account = PersonalAccount("John", "Doe", '12345678911', 'PROM_XYZ')
        assert account.balance == 50.0

    def test_promotion_incorrect(self):
        account = PersonalAccount("John", "Doe", "1234567891", "PROM_XYZ")
        assert account.balance == 0.0
        
    def test_promotion_wrong_format_too_long(self):
        account = PersonalAccount("John", "Doe", '12345678911', "PROM_XYZABC")
        assert account.balance == 0.0

    def test_promotion_wrong_format_too_short(self):
        account = PersonalAccount("John", "Doe", '12345678911', "PROM_A")        
        assert account.balance == 0.0

    def test_promotion_correct_but_too_old(self):
        account = PersonalAccount("John", "Doe", '59010112345', 'PROM_XYZ')
        assert account.balance == 0.0

    def test_promotion_correct_but_after_2000s(self):
        account = PersonalAccount("John", "Doe", '02210112345', 'PROM_XYZ')
        assert account.balance == 50.0

    def test_history_after_operations(self):
        account = PersonalAccount("John", "Doe",'12345678911')
        account.incoming_transfer(500)
        account.outgoing_express_transfer(300)

        assert account.history == [500, -300, -1]
        assert account.balance == 199.0
        






        



    



        
