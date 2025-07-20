from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import create_access_token, hash_password, verify_password
from app.domain.models import User
from app.domain.schemas import Token, UserCreate
from app.infra.database import get_session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=Token,
    summary="Registrar novo usuário",
    description="Cria um novo usuário com nome, e-mail e senha. Retorna um token de autenticação JWT ao finalizar o cadastro com sucesso.",
)
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(User).where(User.email == user_data.email))
    existing_user = result.first()
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
    await session.commit()
    await session.refresh(user)

    token = create_access_token(data={"sub": user.email})
    return Token(access_token=token)


@router.post(
    "/login",
    response_model=Token,
    summary="Autenticar usuário",
    description="Realiza o login com e-mail e senha. Retorna um token JWT caso as credenciais estejam corretas.",
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    result = await session.exec(select(User).where(User.email == form_data.username))
    user = result.first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas"
        )

    token = create_access_token(data={"sub": user.email})
    return Token(access_token=token)
