import requests
import pytest

class TestApiCrud:
    url = "http://127.0.0.1:5000/api/accounts"

    @pytest.fixture(scope="function", autouse=True)
    def set_up(self):
        account_data = {
            "name": "james",
            "surname": "hetfield",
            "pesel": "89092909825"
        }
        response = requests.post(self.url, json=account_data)
        assert response.status_code == 201
        yield
        for account in response.json():
            pesel = account("pesel")
            requests.delete(f"{self.url}/{pesel}")

    def test_create_account(self):
        account_data = {
            "name": "james",
            "surname": "hetfield",
            "pesel": "89092909825"
        }
        response = requests.post(self.url, json=account_data)
        assert response.status_code == 201
        assert response.json()["message"] == "Account created"

    def test_count(self):
        response = requests.get(self.url + "/count")
        assert response.status_code == 200
        assert response.json()["count"] == 1