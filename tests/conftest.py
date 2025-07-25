from typing import AsyncGenerator

import httpx
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from tests.factory.atleta import AtletaModelFactory
from tests.factory.categoria import CategoriaModelFactory
from tests.factory.centro_treinamento import CentroTreinamentoModelFactory
from workout_api.configs.database import get_session
from workout_api.contrib.models import BaseModel
from workout_api.main import app

test_client = TestClient(app=app)


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:17', driver='psycopg') as postgres:
        database_url = postgres.get_connection_url()
        _engine = create_async_engine(database_url)
        yield _engine


@pytest_asyncio.fixture(scope='function')
async def session(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as _session:
        yield _session
    # teardown
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)


@pytest_asyncio.fixture
async def client(
    session: AsyncSession,
) -> AsyncGenerator[httpx.AsyncClient, None]:
    async def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(
        transport=transport, base_url='http://test'
    ) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def bind_factory_session(session: AsyncSession):
    for factory in [
        AtletaModelFactory,
        CategoriaModelFactory,
        CentroTreinamentoModelFactory,
    ]:
        setattr(factory._meta, 'sqlalchemy_session', session)
        setattr(factory._meta, 'sqlalchemy_session_persistence', 'commit')
