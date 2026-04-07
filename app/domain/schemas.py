from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.domain.models import TransactionType


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: str


class AccountRead(BaseModel):
    id: int
    user_id: int
    balance: float

    model_config = ConfigDict(from_attributes=True)


class TransactionRead(BaseModel):
    id: int
    account_id: int
    type: TransactionType
    value: float
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class TransactionResponse(BaseModel):
    message: str
    new_balance: float
    transaction_id: int


class UserRead(BaseModel):
    id: int
    name: str
    email: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
