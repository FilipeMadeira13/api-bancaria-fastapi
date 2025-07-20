from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import get_current_user
from app.domain.models import Account, Transaction, TransactionType, User
from app.domain.schemas import TransactionRead
from app.infra.database import get_session

router = APIRouter(prefix="/statement", tags=["Statement"])


@router.get(
    "/",
    response_model=List[TransactionRead],
    summary="Consultar extrato",
    description="Retorna todas as transações da conta do usuário autenticado. Permite filtrar por tipo (`deposit` ou `withdraw`) e por intervalo de datas (parâmetros `start_date` e `end_date`).",
)
async def read_statement(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    type: Optional[TransactionType] = Query(None),
):
    result = await session.exec(
        select(Account).where(Account.user_id == current_user.id)
    )
    account = result.first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )

    stmt = select(Transaction).where(Transaction.account_id == account.id)

    if start_date:
        stmt = stmt.where(Transaction.timestamp >= start_date)
    if end_date:
        stmt = stmt.where(Transaction.timestamp <= end_date)
    if type:
        stmt = stmt.where(Transaction.type == type)

    result = await session.exec(stmt)
    transactions = result.all()
    return transactions
