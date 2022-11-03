import asyncio

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from app.adapter.in_memory_orm import metadata, start_mappers


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def aio_sqlite_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True, echo=True)
    async with engine.connect() as conn:
        async with conn.begin():
            await conn.run_sync(metadata.create_all)
    start_mappers()
    yield engine
    clear_mappers()


@pytest_asyncio.fixture(scope="function")
async def session_factory(aio_sqlite_engine: AsyncEngine):
    async with aio_sqlite_engine.connect() as conn:
        session_factory = sessionmaker(conn, expire_on_commit=False, autoflush=False, class_=AsyncSession)
        yield session_factory


@pytest_asyncio.fixture(scope="function")
async def session(session_factory: AsyncSession):
    yield session_factory()
