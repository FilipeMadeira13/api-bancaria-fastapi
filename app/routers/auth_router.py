from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.security import create_access_token, hash_password, verify_password
from app.domain.models import User
from app.domain.schemas import Token, UserCreate
from app.infra.database import get_session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado"
        )
    user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    token = create_access_token(data={"sub": user.email})
    return Token(access_token=token)


@router.post("/login", response_model=Token)
def login(user_data: UserCreate, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == user_data.email)).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas"
        )

    token = create_access_token(data={"sub": user.email})
    return Token(access_token=token)
