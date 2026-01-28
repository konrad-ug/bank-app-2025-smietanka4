import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:5000/api/accounts"

@pytest.fixture(scope="module")
def api_url():
    return BASE_URL

def test_persistence_flow(api_url):
    # 1 Create an account
    pesel = "99010112345"
    payload = {
        "name": "Test",
        "surname": "User",
        "pesel": pesel
    }
    
    requests.delete(f"{api_url}/{pesel}")

    resp = requests.post(api_url, json=payload)
    assert resp.status_code == 201

    # 2 Add mock history
    transfer_payload = {"amount": 50.0, "type": "incoming"}
    requests.post(f"{api_url}/{pesel}/transfer", json=transfer_payload)

    # Verify balance
    resp = requests.get(f"{api_url}/{pesel}")
    data = resp.json()[0]
    assert data['balance'] == 50.0

    # 4 Save to DB
    resp = requests.post(f"{api_url}/save")
    assert resp.status_code == 200

    # 5 Clear memory
    requests.delete(f"{api_url}/{pesel}")
    resp = requests.get(f"{api_url}/{pesel}")
    assert resp.status_code == 404

    # 6 Load from DB
    resp = requests.post(f"{api_url}/load")
    assert resp.status_code == 200
    assert "Loaded" in resp.json()["message"]

    # 7 Verify account is back
    resp = requests.get(f"{api_url}/{pesel}")
    assert resp.status_code == 200
    data = resp.json()[0]
    assert data['balance'] == 50.0
    assert data['name'] == "Test"
