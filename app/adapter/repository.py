from abc import ABC, abstractmethod
from typing import Any, Generic, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import Select

from app.domain.models import Base

ModelType = TypeVar("ModelType", bound=Base)


class AbstractRepository(ABC):
    """Abstract Repository For Abstracting Persistence Layer"""

    def add(self, obj):
        self._add(obj)

    async def get(self, ref: Any):
        res = await self._get(ref)
        return res

    async def list(self):
        res = await self._list()
        return res

    @abstractmethod
    def _add(self, obj):
        ...

    @abstractmethod
    async def _get(self, obj):
        ...

    @abstractmethod
    async def _list(self):
        ...


class SqlAlchemyRepository(Generic[ModelType], AbstractRepository):
    def __init__(self, *, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session
        self.seen: set = set()
        self._base_query: Select = select(self.model)

    def _add(self, obj):
        self.session.add(obj)

    async def _get(self, ref):
        q = await self.session.execute(self._base_query.where(self.model.id == ref).limit(1))
        res = q.scalars().first()
        return res

    async def _list(self):
        q = await self.session.execute(self._base_query)
        return q.scalars().all()
