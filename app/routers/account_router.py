from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.security import get_current_user
from app.domain.models import Account, User
from app.infra.database import get_session

router = APIRouter(prefix="/account", tags=["account"])


@router.post("/")
def create_account(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    existing = session.exec(
        select(Account).where(Account.user_id == current_user.id)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário já possui uma conta",
        )

    account = Account(user_id=current_user.id)
    session.add(account)
    session.commit()
    session.refresh(account)
    return account
