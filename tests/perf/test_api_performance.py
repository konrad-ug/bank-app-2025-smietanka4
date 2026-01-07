import requests
import pytest

class TestApiPerf:
    url = "http://127.0.0.1:5000/api/accounts"

    @pytest.fixture(scope="function", autouse=True)
    def set_up(self):
        self.account_data = {
            "name": "James",
            "surname": "Hetfield",
            "pesel": "89092909825"
        }

        requests.delete(f"{self.url}/{self.account_data['pesel']}")

        yield

        all_account_response = requests.get(self.url)
        if all_account_response.status_code == 200:
            for account in all_account_response.json():
                pesel = account['pesel']
                requests.delete(f"{self.url}/{pesel}")

    def test_account_creation_and_delete(self):
        self.account_data = {
            "name": "James",
            "surname": "Hetfield",
            "pesel": "89092909825"
        }

        for _ in range(100):
            creation = requests.post(self.url, json=self.account_data,timeout = 0.5)
            assert creation.status_code == 201
            response = requests.get(f"{self.url}/{self.account_data['pesel']}", timeout=0.5)
            assert response.status_code == 200

            delete = requests.delete(f"{self.url}/{self.account_data['pesel']}", timeout=0.5)
            assert delete.status_code == 200

    def test_account_creation_and_100_transfers(self):
        self.account_data = {
            "name": "James",
            "surname": "Hetfield",
            "pesel": "89092909825"
        }

        creation = requests.post(self.url, json=self.account_data, timeout=0.5)

        assert creation.status_code == 201

        transfer_amount = 10
        self.transfer_data = {
            "amount": transfer_amount,
            "type": "incoming"
        }

        for _ in range(100):
            transfer = requests.post(f"{self.url}/{self.account_data['pesel']}/transfer",json=self.transfer_data, timeout=0.5)
            assert transfer.status_code == 200

            response = requests.get(f"{self.url}/{self.account_data['pesel']}", timeout=0.5)
            assert response.status_code == 200

        final_response = requests.get(f"{self.url}/{self.account_data['pesel']}", timeout=0.5)
        assert final_response.status_code == 200

        account_info = final_response.json()[0]

        current_balance = account_info['balance']
        expected_balance = transfer_amount * 100

        assert current_balance == expected_balance  

        delete = requests.delete(f"{self.url}/{self.account_data['pesel']}")
        assert delete.status_code == 200

