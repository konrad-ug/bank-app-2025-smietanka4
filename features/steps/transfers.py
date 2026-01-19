from behave import *
import requests

URL = "http://localhost:5000"


@when('I perform "{transfer_type}" transfer of "{amount}" to account "{pesel}"')
def perform_transfer(context, transfer_type, amount, pesel):
    """Performs a transfer of specified type and amount"""
    json_body = {
        "amount": float(amount),
        "type": transfer_type
    }
    
    context.last_response = requests.post(
        URL + f"/api/accounts/{pesel}/transfer",
        json=json_body
    )


@when('I perform invalid type "{transfer_type}" transfer of "{amount}" to account "{pesel}"')
def perform_invalid_transfer_type(context, transfer_type, amount, pesel):
    """Performs a transfer with invalid type"""
    json_body = {
        "amount": float(amount),
        "type": transfer_type
    }
    
    context.last_response = requests.post(
        URL + f"/api/accounts/{pesel}/transfer",
        json=json_body
    )


@then('Account "{pesel}" has balance equal to "{expected_balance}"')
def check_account_balance_equal(context, pesel, expected_balance):
    """Verifies account balance matches expected value"""
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    
    account_data = response.json()
    actual_balance = float(account_data[0]["balance"])
    expected_balance = float(expected_balance)
    
    assert actual_balance == expected_balance, \
        f"Balance mismatch. Expected: {expected_balance}, Got: {actual_balance}"


@then('Account "{pesel}" has balance less than "{max_balance}"')
def check_account_balance_less_than(context, pesel, max_balance):
    """Verifies account balance is less than specified amount"""
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    
    account_data = response.json()
    actual_balance = float(account_data[0]["balance"])
    max_balance = float(max_balance)
    
    assert actual_balance < max_balance


@then('Transfer should fail')
def transfer_should_fail(context):
    """Verifies the last transfer failed"""
    assert context.last_response.status_code >= 400