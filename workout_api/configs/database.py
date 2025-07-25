from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from workout_api.configs.settings import settings

engine = create_async_engine(settings.DB_URL, echo=False)


async def get_session() -> AsyncGenerator:  # pragma: no cover
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
