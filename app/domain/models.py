from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


class Base:
    id: str


@dataclass
class User(Base):
    id: str
    name: str
    age: int  # Index
    gender: str  # Index
    phone: str
    email: str
    photo: list = field(default_factory=list)
    description: str = ""
    school: str | None = None
    job: str | None = None

    # self means the user of a row
    users_liked_by_self: set["User"] = field(default_factory=set)  # Mapped
    users_who_like_self: set["User"] = field(default_factory=set)

    users_disliked_by_self: set["User"] = field(default_factory=set)
    users_who_dislike_self: set["User"] = field(default_factory=set)

    create_dt: datetime = field(init=False)
    update_dt: datetime = field(init=False)
    events: deque = deque()

    @classmethod
    def create_user(cls, **kwargs):
        return cls(id=str(uuid4()), **kwargs)

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, User):
            return False
        return self.id == __o.id
