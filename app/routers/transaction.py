from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import get_current_user
from app.domain.models import Account, Transaction, TransactionType, User
from app.domain.schemas import TransactionRead
from app.infra.database import get_session

router = APIRouter(prefix="/transaction", tags=["transaction"])


class TransactionInput(BaseModel):
    type: TransactionType
    value: float = Field(..., gt=0, description="Valor positivo")


@router.post(
    "/",
    summary="Registrar transação",
    description="Registra uma transação de depósito ou saque para o usuário autenticado. Saques requerem saldo suficiente. Apenas valores positivos são aceitos.",
)
async def create_transaction(
    data: TransactionInput,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    result = await session.exec(
        select(Account).where(Account.user_id == current_user.id)
    )
    account = result.first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada"
        )

    if data.type == TransactionType.withdraw and data.value > account.balance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Saldo insuficiente"
        )

    if data.type == TransactionType.deposit:
        account.balance += data.value
    else:
        account.balance -= data.value

    transaction = Transaction(account_id=account.id, type=data.type, value=data.value)
    session.add(transaction)
    session.add(account)
    await session.commit()
    await session.refresh(transaction)

    return {
        "message": f"{data.type.value.capitalize()} realizado com sucesso",
        "new_balance": account.balance,
        "transaction_id": transaction.id,
    }
