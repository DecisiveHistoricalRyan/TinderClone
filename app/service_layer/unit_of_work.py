from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapter.repository import AbstractRepository, SqlAlchemyRepository
from app.domain import models
from core.db import async_autocommit_session, async_transactional_session

DEFAULT_SESSION_TRANSACTIONAL_SESSION_FACTORY = async_transactional_session
DEFAULT_SESSION_AUTOCOMMIT_SESSION_FACTORY = async_autocommit_session


class AbstractUnitOfWork(ABC):
    users: AbstractRepository

    async def commit(self):
        await self._commit()

    async def rollback(self):
        await self._rollback()

    @abstractmethod
    async def _commit(self):
        ...

    @abstractmethod
    async def _rollback(self):
        ...

    async def __aenter__(self):
        ...

    async def __aexit__(self, *args, **kwargs):
        ...


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=None):
        self.session_factory = (
            DEFAULT_SESSION_TRANSACTIONAL_SESSION_FACTORY if session_factory is None else session_factory
        )

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()
        self.users: SqlAlchemyRepository = SqlAlchemyRepository(model=models.User, session=self.session)
