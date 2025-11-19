from src.account_registry import AccountRegistry
import pytest

class TestAccountRegistry:

    @pytest.fixture
    def account_registry(self):
        return AccountRegistry()

    def test_account_registry_creation(self, account_registry):
        assert len(account_registry.accounts) == 0 

    def test_account_registry_add_account(self, account_registry, example_account):
        account_registry.add_account(example_account)

        assert account_registry.account[-1] == example_account

    def test_account_registry_search_account(self, account_registry, example_account_pesel):
        account_registry.get_account_by_pesel("")