from datetime import datetime
from typing import Optional

from fastapi import Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.core.security import get_current_user
from app.domain.models import Transaction, TransactionType, User
from app.infra.database import get_session


def get_statement(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    type: Optional[TransactionType] = Query(None),
):
    account = current_user.account
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

    transactions = session.exec(stmt).all()
    return transactions
