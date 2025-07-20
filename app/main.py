from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.domain.models import Account, Transaction, User
from app.infra.database import create_db_and_tables
from app.routers import account, auth, statement, transaction


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(
    summary="API de operações bancárias modernas e seguras",
    contact={
        "name": "Carlos Filipe Madeira de Souza",
        "url": "https://github.com/FilipeMadeira13",
        "email": "cfilipemadeira@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(account.router)
app.include_router(transaction.router)
app.include_router(statement.router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="API Bancária Assíncrona",
        description="""
        API RESTful desenvolvida com FastAPI para gerenciamento de operações bancárias.

        Funcionalidades:
        - Registro e autenticação de usuários com JWT
        - Criação de contas bancárias
        - Depósitos e saques com validações
        - Consulta de extrato com filtros
        - Projeto estruturado com Clean Architecture

        Todos os endpoints protegidos utilizam autenticação via JWT.
        """,
        version="1.0.0",
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
