import pytest
from fastapi import status


def register_and_login(client):
    reg_payload = {
        "name": "Filipe",
        "email": "filipe@teste.com",
        "password": "123456",
    }
    client.post("/auth/register", json=reg_payload)
    login_resp = client.post(
        "/auth/login",
        data={"username": reg_payload["email"], "password": reg_payload["password"]},
    )
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_account_success(client):
    headers = register_and_login(client)

    resp = client.post("/account/", headers=headers)
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert data["user_id"] == 1
    assert data["balance"] == 0


def test_create_account_duplicate(client):
    headers = register_and_login(client)

    # 1ª criação
    client.post("/account/", headers=headers)
    # 2ª criação deve falhar
    resp = client.post("/account/", headers=headers)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json()["detail"] == "Usuário já possui uma conta"
