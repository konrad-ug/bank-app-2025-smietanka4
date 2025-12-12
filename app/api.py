from flask import Flask, request, jsonify
from src.account_registry import AccountRegistry
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount
from src.account import Account

app = Flask(__name__)

registry = AccountRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")

    existing_account = registry.get_account_by_pesel(data['pesel'])
    if existing_account:
        return jsonify({"message": "Account with this PESEL already exists"}), 409
    
    account = PersonalAccount(data['name'], data['surname'], data['pesel'])
    registry.add_account(account)
    return jsonify({'message': "Account created"}), 201


@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    print("Get all accounts request received")
    accounts = registry.get_all_accounts()
    accounts_data = [{"name": acc.first_name, "surname": acc.last_name, "pesel": acc.pesel, "balance": acc.balance} for acc in accounts]
    return jsonify(accounts_data), 200



@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    print("Get account count request received")
    count = registry.get_amount_of_accounts()
    count_data = {"count": count}
    return jsonify(count_data), 200



@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_accounts_by_pesel(pesel):
    print(f"Get account by pesel: {pesel} request received")
    account = registry.get_account_by_pesel(pesel)

    if not account:
        return jsonify({"error": "Account not found"}), 404
    
    account_data = [{"name": account.first_name, "surname": account.last_name, "pesel": account.pesel, "balance": account.balance}]
    return jsonify(account_data), 200



@app.route('/api/accounts/<pesel>', methods=['PATCH'])
def update_account(pesel):
    account = registry.get_account_by_pesel(pesel)
    if not account:
        return jsonify({"error": f"Account with pesel {pesel} does not exist"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    new_name = data.get('name', account.first_name)
    new_surname = data.get('surname', account.last_name)
    print(f"Update account by pesel: {pesel} request received")
    registry.update_account(new_name, new_surname, pesel)
    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    print(f'Delete account by pesel: {pesel} request received')

    account = registry.get_account_by_pesel(pesel)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    
    registry.delete_account_by_pesel(pesel)
    return jsonify({"message": "Account deleted"}), 200

@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def make_transfer(pesel):
    account = registry.get_account_by_pesel(pesel)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    
    data = request.get_json()
    if not data or 'amount' not in data or 'type' not in data:
        return jsonify({"error": "Missing amount or type"}), 400
    
    amount = data['amount']
    transfer_type = data['type']

    success = False

    if transfer_type == 'incoming':
        account.incoming_transfer(amount)
        success = True
    elif transfer_type == "outgoing":
        success = account.outgoing_transfer(amount)
    elif transfer_type == "express":
        success = account.outgoing_express_transfer(amount)
    else:
        return jsonify({"message": "Invalid transfer type"}), 400
    
    if success:
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
    else:
        return jsonify({"error": "Insufficient funds or transfer failed"}), 422