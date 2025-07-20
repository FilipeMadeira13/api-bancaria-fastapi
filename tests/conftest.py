import asyncio

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, text
from sqlmodel.ext.asyncio.session import AsyncSession

from app.infra.database import get_session
from app.main import app

DATABASE_URL = "sqlite+aiosqlite:///:memory:?cache=shared"

test_engine = create_async_engine(
    DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    await test_engine.dispose()


@pytest.fixture
async def session():
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture(autouse=True)
def clean_tables():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(clean_tables_async())
    loop.close()


async def clean_tables_async():
    async with test_engine.begin() as conn:
        tables = ['"user"', '"account"', '"transaction"']
        for table in tables:
            await conn.execute(text(f"DELETE FROM {table}"))
        await conn.commit()


@pytest.fixture
def client():
    app.dependency_overrides[get_session] = override_get_session
    return TestClient(app)


async def override_get_session():
    async with TestingSessionLocal() as session:
        yield session
