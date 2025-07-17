from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: str
