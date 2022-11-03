from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class User:

    id: UUID
    name: str
    age: int  # Index
    gender: str  # Index
    school: str | None
    job: str | None
    phone: str
    email: str
    photo: list = field(default_factory=list)
    description: str = ""

    # self means the user of a row
    users_liked_by_self: list["User"] = field(default_factory=list)  # Mapped
    users_who_like_self: list["User"] = field(default_factory=list)

    users_disliked_by_self: list["User"] = field(default_factory=list)
    users_who_dislike_self: list["User"] = field(default_factory=list)

    create_dt: datetime = field(init=False)
    update_dt: datetime = field(init=False)
    events: deque = deque()
