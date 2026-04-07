from fastapi import status

from app.domain.models import TransactionType
from tests.test_account import register_and_login


def create_transaction(client, headers, type_, value):
    return client.post(
        "/transaction/",
        json={
            "type": type_.value if hasattr(type_, "value") else type_,
            "value": value,
        },
        headers=headers,
    )


def setup_user_account(client):
    headers = register_and_login(client)
    client.post("/account/", headers=headers)
    return headers


def test_deposit_and_withdraw_flow(client):
    headers = setup_user_account(client)

    deposit_resp = create_transaction(client, headers, TransactionType.deposit, 100)
    assert deposit_resp.status_code == status.HTTP_201_CREATED
    assert deposit_resp.json()["new_balance"] == 100

    withdraw_resp = create_transaction(client, headers, TransactionType.withdraw, 40)
    assert withdraw_resp.status_code == status.HTTP_201_CREATED
    assert withdraw_resp.json()["new_balance"] == 60


def test_withdraw_insufficient_funds(client):
    headers = setup_user_account(client)

    response = create_transaction(client, headers, TransactionType.withdraw, 10)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Saldo insuficiente"
