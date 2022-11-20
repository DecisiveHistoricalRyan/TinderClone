from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class User:
    id: UUID
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
    users_liked_by_self: list["User"] = field(default_factory=list)  # Mapped
    users_who_like_self: list["User"] = field(default_factory=list)

    users_disliked_by_self: list["User"] = field(default_factory=list)
    users_who_dislike_self: list["User"] = field(default_factory=list)

    create_dt: datetime = field(init=False)
    update_dt: datetime = field(init=False)
    events: deque = deque()

    @classmethod
    def create_user(cls, **kwargs):
        return cls(id=str(uuid4()), **kwargs)
