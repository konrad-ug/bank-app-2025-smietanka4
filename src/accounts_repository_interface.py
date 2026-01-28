from abc import ABC, abstractmethod

class AccountsRepository(ABC):
    @abstractmethod
    def save_all(self, accounts: list): # pragma: no cover
        pass

    @abstractmethod
    def load_all(self) -> list: # pragma: no cover
        pass