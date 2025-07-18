from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.core.security import get_current_user
from app.domain.models import Transaction, TransactionType, User
from app.domain.schemas import TransactionRead, UserRead
from app.infra.database import get_session
from app.use_cases.get_statement import get_statement

router = APIRouter(prefix="/statement", tags=["Statement"])


@router.get("/", response_model=List[TransactionRead])
def read_statement(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    type: Optional[TransactionType] = Query(None),
):
    return get_statement(session, current_user, start_date, end_date, type)
