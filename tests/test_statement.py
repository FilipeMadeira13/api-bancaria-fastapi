from datetime import datetime, timedelta, timezone

from fastapi import status

from app.domain.models import TransactionType
from tests.test_account import register_and_login


def setup_user_account(client):
    headers = register_and_login(client)
    client.post("/account/", headers=headers)
    return headers


def create_transaction(client, headers, type_, value):
    payload = {"type": type_, "value": value}
    return client.post("/transaction/", json=payload, headers=headers)


def test_statement_all_and_filters(client):
    headers = setup_user_account(client)

    # cria 2 depósitos e 1 saque
    create_transaction(client, headers, TransactionType.deposit, 100)
    create_transaction(client, headers, TransactionType.withdraw, 30)
    create_transaction(client, headers, TransactionType.deposit, 50)

    # ---- extrato completo ----
    resp_all = client.get("/statement", headers=headers)
    assert resp_all.status_code == status.HTTP_200_OK
    assert len(resp_all.json()) == 3

    # ---- filtra por tipo=deposit ----
    resp_dep = client.get("/statement?type=deposit", headers=headers)
    values = [t["value"] for t in resp_dep.json()]
    assert len(values) == 2 and 100 in values and 50 in values

    # ---- filtra por intervalo de datas (últimos 10 seg) ----
    start = (datetime.now(timezone.utc) - timedelta(seconds=10)).replace(microsecond=0)
    iso_start = start.isoformat().replace("+00:00", "Z")
    resp_date = client.get(f"/statement?start_date={iso_start}", headers=headers)
    assert resp_date.status_code == status.HTTP_200_OK

    assert len(resp_date.json()) == 3
