from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine

from app.domain.models import Account, Transaction, User
from app.infra.database import create_db_and_tables
from app.routers import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router.router)

sqlite_url = "sqlite:///bank.db"
engine = create_engine(sqlite_url, echo=True)


@app.get("/")
async def root():
    return {"message": "API Bancária Assíncrona"}
