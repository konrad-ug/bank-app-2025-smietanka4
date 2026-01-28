import unittest
from unittest.mock import MagicMock, patch
from src.mongo_accounts_repository import MongoAccountsRepository
from src.personal_account import PersonalAccount

class TestMongoAccountsRepository(unittest.TestCase):
    def setUp(self):
        self.mock_collection = MagicMock()
        self.repo = MongoAccountsRepository(collection=self.mock_collection)

    def test_save_all_clears_collection_and_saves_accounts(self):
        account1 = PersonalAccount("Jan", "Kowalski", "90010112345")
        account1.balance = 100.0
        account2 = PersonalAccount("Anna", "Nowak", "92020212345")
        account2.balance = 200.0
        accounts = [account1, account2]

        self.repo.save_all(accounts)

        self.mock_collection.delete_many.assert_called_once_with({})
        
        self.assertEqual(self.mock_collection.update_one.call_count, 2)
        
        call_args_list = self.mock_collection.update_one.call_args_list
        
        first_call = call_args_list[0]
        self.assertEqual(first_call[0][0], {"pesel": "90010112345"})
        self.assertEqual(first_call[0][1], {"$set": account1.to_dict()})
        self.assertEqual(first_call[1]['upsert'], True)

    def test_save_all_empty_list_only_clears_collection(self):
        self.repo.save_all([])
        self.mock_collection.delete_many.assert_called_once_with({})
        self.mock_collection.update_one.assert_not_called()

    def test_load_all_returns_account_objects(self):
        mock_data = [
            {
                "first_name": "Jan",
                "last_name": "Kowalski",
                "pesel": "90010112345",
                "balance": 100.0,
                "history": [100.0],
                "type": "personal"
            },
            {
                "first_name": "Anna",
                "last_name": "Nowak",
                "pesel": "92020212345",
                "balance": 200.0,
                "history": [],
                "type": "personal"
            }
        ]
        self.mock_collection.find.return_value = mock_data

        result = self.repo.load_all()

        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], PersonalAccount)
        self.assertEqual(result[0].first_name, "Jan")
        self.assertEqual(result[0].balance, 100.0)
        self.assertEqual(result[0].history, [100.0])

if __name__ == '__main__':
    unittest.main()
