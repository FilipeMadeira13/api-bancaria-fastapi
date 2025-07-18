from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import SQLModel, create_engine

from app.domain.models import Account, Transaction, User
from app.infra.database import create_db_and_tables
from app.routers import (
    account_router,
    auth_router,
    statement_router,
    transaction_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router.router)
app.include_router(account_router.router)
app.include_router(transaction_router.router)
app.include_router(statement_router.router)

sqlite_url = "sqlite:///bank.db"
engine = create_engine(sqlite_url, echo=True)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="API Bancária Assíncrona",
        version="1.0.0",
        description="Desafio com autenticação JWT",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
