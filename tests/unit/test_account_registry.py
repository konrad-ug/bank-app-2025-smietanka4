from src.account_registry import AccountRegistry
from src.personal_account import PersonalAccount
import pytest

class TestAccountRegistry:

    @pytest.fixture
    def registry(self):
        return AccountRegistry()

    def test_add_and_get_account(self, registry: AccountRegistry):
        account = PersonalAccount("John", "Doe", "12345678911")
        registry.add_account(account)
        retrieved_account = registry.get_account_by_pesel("12345678911")
        assert retrieved_account == account

    def test_get_account_not_found(self, registry: AccountRegistry):
        retrieved_account = registry.get_account_by_pesel("00000000000")
        assert retrieved_account is None

    def test_get_all_account(self, registry: AccountRegistry):
        account1 = PersonalAccount("John", "Doe", "12345678911")
        account2 = PersonalAccount("John", "Nowak", "12345678910")
        registry.add_account(account1)
        registry.add_account(account2)
        all_accounts = registry.get_all_accounts()
        registry_length = registry.get_amount_of_accounts()
        assert all_accounts == [account1, account2]
        assert registry_length == 2

    def test_get_all_accounts_but_empty(self, registry: AccountRegistry):
        all_accounts = registry.get_all_accounts()
        registry_length = registry.get_amount_of_accounts()
        assert all_accounts == []
        assert registry_length == 0

    def test_update_account_by_pesel(self, registry: AccountRegistry):
        account1 = PersonalAccount("John", "Doe", "12345678911")
        registry.add_account(account1)
        registry.update_account("Karol", "Nowak", '12345678911')
        assert account1.first_name == "Karol"
        assert account1.last_name == "Nowak"
        assert account1.pesel == "12345678911"

    def test_delete_account_by_pesel(self, registry: AccountRegistry):
        account1 = PersonalAccount("John", "Doe", "12345678911")
        account2 = PersonalAccount("John", "Nowak", "12345678910")
        registry.add_account(account1)
        registry.add_account(account2)
        registry.delete_account_by_pesel('12345678910')
        registry.delete_account_by_pesel('12345678910')
        all_accounts = registry.get_all_accounts()
        registry_length = registry.get_amount_of_accounts()
        assert all_accounts == [account1]
        assert registry_length == 1

        