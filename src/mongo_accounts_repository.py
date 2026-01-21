import os
from pymongo import MongoClient
from src.accounts_repository_interface import AccountsRepository
from src.personal_account import PersonalAccount


def MongoAccountsRepository(AccountsRepository):
    def __init__(self, mongo_uri=None, db_name=None, collection_name=None, collection=None):
        if collection is not None:
            self._collection = collection
            return

        mongo_uri = mongo_uri or os.getenv("MONGO_URI", "mongodb://localhost:27017")
        db_name = db_name or os.getenv("MONGO_DB", "bank_app")
        collection_name = collection_name or os.getenv("MONGO_COLLECTION", "accounts")

        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self._collection = self.db[collection_name]

    def save_all(self, accounts: list):
        self._collection.delete_many({})

        if not accounts:
            return

        for account in accounts:
            self._collection.update_one(
                {"pesel": account.pesel},
                {"set": account.to_dict()},
                upsert=True
            )

    def load_all(self) -> list:
        documents = self._collection.find({}, {"_id": 0})
        accounts = []

        for doc in documents:
            if doc.get("type") == "personal":
                acc = PersonalAccount(doc["first_name"], doc["last_name"], doc["pesel"])
                acc.balance = doc["balance"]
                acc.history = doc["history"]
                accounts.append(acc)

        return accounts