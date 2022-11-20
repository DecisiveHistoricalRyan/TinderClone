from sqlalchemy.ext.asyncio import AsyncSession

from app.domain import models
from app.service_layer.unit_of_work import SqlAlchemyRepository, SqlAlchemyUnitOfWork


class FakeSqlUnitOfWork(SqlAlchemyUnitOfWork):
    def __init__(self, session_factory=None):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory
        self.users: SqlAlchemyRepository = SqlAlchemyRepository(model=models.User, session=self.session)
        return self

    async def __aexit__(self, *args, **kwargs):
        ...
