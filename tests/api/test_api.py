import requests
import pytest

class TestApiCrud:
    url = "http://127.0.0.1:5000/api/accounts"

    @pytest.fixture(scope="function", autouse=True)
    def set_up(self):
        self.account_data = {
            "name": "james",
            "surname": "hetfield",
            "pesel": "89092909825"
        }
        requests.delete(f"{self.url}/{self.account_data['pesel']}")

        response = requests.post(self.url, json=self.account_data)
        assert response.status_code == 201

        yield

        all_account_response = requests.get(self.url)
        if all_account_response.status_code == 200:
            for account in all_account_response.json():
                pesel = account["pesel"]
                requests.delete(f"{self.url}/{pesel}")

    def test_create_account(self):
        account_data = {
            "name": "james",
            "surname": "hetfield",
            "pesel": "89092909825"
        }

        requests.delete(f"{self.url}/{account_data['pesel']}")
        response = requests.post(self.url, json=account_data)
        assert response.status_code == 201
        assert response.json()["message"] == "Account created"

    def test_count(self):
        response = requests.get(self.url + "/count")
        assert response.status_code == 200
        assert response.json()["count"] == 1