from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class TransactionType(str, Enum):
    deposit = "deposit"
    withdraw = "withdraw"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    hashed_password: str

    account: Optional["Account"] = Relationship(back_populates="user")


class Account(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    balance: float = 0.0

    user: Optional[User] = Relationship(back_populates="account")
    transactions: List["Transaction"] = Relationship(back_populates="account")


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    account_id: int = Field(foreign_key="account.id")
    type: TransactionType
    value: float
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))

    account: Optional[Account] = Relationship(back_populates="transactions")
