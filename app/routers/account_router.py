from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import get_current_user
from app.domain.models import Account, User
from app.infra.database import get_session

router = APIRouter(prefix="/account", tags=["account"])


@router.post(
    "/",
    summary="Criar conta bancária",
    description="Cria uma conta corrente para o usuário autenticado. Um usuário pode ter apenas uma conta vinculada.",
)
async def create_account(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    result = await session.exec(
        select(Account).where(Account.user_id == current_user.id)
    )
    existing = result.first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário já possui uma conta",
        )

    account = Account(user_id=current_user.id)
    session.add(account)
    await session.commit()
    await session.refresh(account)
    return account
