import asyncio
import copy
import uuid
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from app.adapter.in_memory_orm import metadata, start_mappers
from app.domain.enums import Gender
from app.domain.models import User
from app.entrypoints import deps
from app.tests.fakes import FakeSqlAlchemyUnitOfWork


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
        session_factory: sessionmaker = sessionmaker(
            conn,  # type: ignore
            expire_on_commit=False,
            autoflush=False,
            class_=AsyncSession,
        )
        yield session_factory


@pytest_asyncio.fixture(scope="function")
async def session(session_factory: sessionmaker):
    session: AsyncSession = session_factory()
    yield session
    for table in metadata.tables.keys():
        delete_stmt = f"DELETE FROM {table};"
        await session.execute(text(delete_stmt))
    await session.commit()
    await session.close()


@pytest_asyncio.fixture(scope="function")
def user_id() -> str:
    return str(uuid.uuid4())


@pytest_asyncio.fixture(scope="function")
def user_name() -> str:
    return "Migo"


@pytest_asyncio.fixture(scope="function")
def user_age() -> int:
    return 32


@pytest_asyncio.fixture(scope="function")
def user_gender() -> str:
    return Gender.Male.value


@pytest_asyncio.fixture(scope="function")
def user_school() -> str:
    return "KNSU"


@pytest_asyncio.fixture(scope="function")
def user_phone() -> str:
    return "010-0000-0000"


@pytest_asyncio.fixture(scope="function")
def user_description() -> str:
    return "This is me"


@pytest_asyncio.fixture(scope="function")
def user_email() -> str:
    return "saka90030@gmail.com"


@pytest_asyncio.fixture(scope="function")
def user_photo() -> list[str]:
    return ["https://i.imgur.com/RefcteE.jpeg"]


@pytest_asyncio.fixture(scope="function")
def user_job() -> str:
    return "programmer"


@pytest_asyncio.fixture(scope="function")
async def user(
    user_id: str,
    user_name: str,
    user_age: int,
    user_gender: str,
    user_school: str,
    user_phone: str,
    user_description: str,
    user_email: str,
    user_photo: list[str],
    user_job: str,
) -> AsyncGenerator:
    user = User(
        id=user_id,
        name=user_name,
        age=user_age,
        gender=user_gender,
        school=user_school,
        phone=user_phone,
        description=user_description,
        email=user_email,
        photo=user_photo,
        job=user_job,
    )
    yield user


user2 = copy.deepcopy(user)


@pytest_asyncio.fixture(scope="function")
def two_users(user, user2):
    user.id = str(uuid.uuid4())
    yield user, user2


@pytest.fixture(scope="function")
def client(session: AsyncSession) -> Generator:
    from app.main import app

    app.dependency_overrides[deps.get_uow] = lambda: FakeSqlAlchemyUnitOfWork(session_factory=session)

    with TestClient(app) as tc:
        yield tc
