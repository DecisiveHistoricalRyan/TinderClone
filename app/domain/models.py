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

    likes_on: list = field(default_factory=list)  # Mapped
    liked_by: list = field(default_factory=list)

    dislikes_on: list = field(default_factory=list)
    disliked_by: list = field(default_factory=list)

    create_dt: datetime = field(init=False)
    update_dt: datetime = field(init=False)
    events: deque = deque()
