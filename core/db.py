import os

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine: AsyncEngine | None = None
autocommit_engine: AsyncEngine | None = None


if os.getenv("STAGE") not in ("ci_testing", "local"):
    DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(
        settings.POSTGRES_PROTOCOL,
        settings.POSTGRES_USER,
        settings.POSTGRES_PASSWORD,
        settings.POSTGRES_SERVER,
        settings.POSTGRES_PORT,
        settings.POSTGRES_DB,
    )
    engine = create_async_engine(DATABASE_URI, future=True)

async_transactional_session: sessionmaker = sessionmaker(
    engine,  # type: ignore
    expire_on_commit=False,
    autoflush=False,
    class_=AsyncSession,
)
autocommit_engine = engine.execution_options(isolation_level="AUTOCOMMIT") if engine is not None else None
async_autocommit_session: sessionmaker = sessionmaker(
    autocommit_engine,  # type: ignore
    expire_on_commit=False,
    class_=AsyncSession,
)
