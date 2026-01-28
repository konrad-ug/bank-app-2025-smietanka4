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

    def test_persistence_flow():
        base_url = "http://127.0.0.1:5000/api/accounts"
        
        pesel = "99010112345"
        payload = {
            "name": "Test",
            "surname": "User",
            "pesel": pesel
        }
        
        requests.delete(f"{base_url}/{pesel}")

        resp = requests.post(base_url, json=payload)
        assert resp.status_code == 201

        transfer_payload = {"amount": 50.0, "type": "incoming"}
        requests.post(f"{base_url}/{pesel}/transfer", json=transfer_payload)

        resp = requests.get(f"{base_url}/{pesel}")
        data = resp.json()[0]
        assert data['balance'] == 50.0

        resp = requests.post(f"{base_url}/save")
        assert resp.status_code == 200

        requests.delete(f"{base_url}/{pesel}")
        resp = requests.get(f"{base_url}/{pesel}")
        assert resp.status_code == 404

        resp = requests.post(f"{base_url}/load")
        assert resp.status_code == 200
        assert "Loaded" in resp.json()["message"]

        resp = requests.get(f"{base_url}/{pesel}")
        assert resp.status_code == 200
        data = resp.json()[0]
        assert data['balance'] == 50.0
        assert data['name'] == "Test"
