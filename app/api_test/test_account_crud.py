import requests
import pytest

class TestAccountCrud:
      base_url = "http://127.0.0.1:5000/api/accounts"

      @pytest.fixture(scope="function", autouse=True)
      def set_up(self):
            self.account_data = {
                  "name": "james",
                  "surname": "hetfield",
                  "pesel": "89092909825"
            }

            requests.delete(f"{self.base_url}/{self.account_data['pesel']}")

            response = requests.post(self.base_url, json=self.account_data)
            assert response.status_code == 201

            yield

            all_accounts_response = requests.get(self.base_url)
            if all_accounts_response.status_code == 200:
                  for account in all_accounts_response.json():
                        pesel = account["pesel"]
                        requests.delete(f"{self.base_url}/{pesel}")

      # test na wyszukiwanie konta
      def test_get_account_by_pesel(self):
            pesel = self.account_data["pesel"]
            response = requests.get(f"{self.base_url}/{pesel}")

            assert response.status_code == 200

            account = response.json()[0]
            assert account['name'] == self.account_data["name"]
            assert account["surname"] == self.account_data["surname"]
            assert account["pesel"] == pesel

      # test na konto ktorego nie ma
      def test_get_non_existent_account(self):
            fake_pesel = "00000000000"

            response = requests.get(f"{self.base_url}/{fake_pesel}")

            assert response.status_code == 404
            assert response.json()["error"] == "Account not found"

      # test na update konta
      def test_update_account(self):
            pesel = self.account_data["pesel"]
            new_data = {"surname": "Ulrich"}

            update_response = requests.patch(f"{self.base_url}/{pesel}", json=new_data)
            assert update_response.status_code == 200
            assert update_response.json()["message"] == 'Account updated'

            get_response = requests.get(f"{self.base_url}/{pesel}")
            updated_account = get_response.json()[0]

            assert updated_account["surname"] == "Ulrich"
            assert updated_account["name"] == "james"
      
      # test na usuwanie konta
      def test_delete_account(self):
            pesel = self.account_data['pesel']

            delete_response = requests.delete(f"{self.base_url}/{pesel}")
            assert delete_response.status_code == 200
            assert delete_response.json()["message"] == "Account deleted"

            get_response = requests.get(f"{self.base_url}/{pesel}")
            assert get_response.status_code == 404

      # test na feature 16, unikalny pesel
      def test_create_duplicate_account(self):
            response = requests.post(self.base_url, json=self.account_data)

            assert response.status_code == 409

      # ========== TESTY -> FEATURE 17 ==========
      def test_incoming_transfer(self):
            pesel = self.account_data["pesel"]
            payload = {"amount": 100, "type": "incoming"}

            response = requests.post(f"{self.base_url}/{pesel}/transfer", json=payload)

            assert response.status_code == 200

            get_response = requests.get(f"{self.base_url}/{pesel}")
            account = get_response.json()[0]
            assert account["balance"] == 100

      def test_outgoing_transfer_success(self):
            pesel = self.account_data["pesel"]

            requests.post(f"{self.base_url}/{pesel}/transfer", json={"amount": 500, "type": "incoming"})

            payload = {"amount": 200, "type": "outgoing"}
            response = requests.post(f"{self.base_url}/{pesel}/transfer", json=payload)
            assert response.status_code == 200

            get_response = requests.get(f"{self.base_url}/{pesel}")
            account = get_response.json()[0]
            assert account["balance"] == 300

      def test_outgoing_transfer_insufficient_funds(self):
            pesel = self.account_data["pesel"]

            payload = {"amount": 100, "type": "outgoing"}
            response = requests.post(f"{self.base_url}/{pesel}/transfer", json=payload)

            assert response.status_code == 422

            get_response = requests.get(f"{self.base_url}/{pesel}")
            assert get_response.json()[0]["balance"] == 0

      def test_express_transfer_success(self):
            pesel = self.account_data['pesel']

            requests.post(f"{self.base_url}/{pesel}/transfer", json={"amount": 1000, "type": "incoming"})

            payload = {"amount": 500, "type": "express"}
            response = requests.post(f"{self.base_url}/{pesel}/transfer", json=payload)
            assert response.status_code == 200

            get_response = requests.get(f"{self.base_url}/{pesel}")
            balance = get_response.json()[0]["balance"]
            assert balance <= 500

      def test_invalid_transfer_type(self):
            pesel = self.account_data["pesel"]
            payload = {"amount": 100, "type": "crypto_fraud"}

            response = requests.post(f"{self.base_url}/{pesel}/transfer", json=payload)
            assert response.status_code == 400

      def test_transfer_account_not_found(self):
            fake_pesel = "99999999999"
            payload = {"amount": 100, "type": "incoming"}

            response = requests.post(f"{self.base_url}/{fake_pesel}/transfer", json=payload)
            assert response.status_code == 404