from fastapi import status


def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={"name": "Filipe", "email": "filipe@teste.com", "password": "123456"},
    )
    print("JSON de resposta:", response.json())
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 10


def test_login_user(client):
    client.post(
        "/auth/register",
        json={"name": "Filipe", "email": "filipe@teste.com", "password": "123456"},
    )

    response = client.post(
        "/auth/login",
        data={"username": "filipe@teste.com", "password": "123456"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
