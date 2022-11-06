from dataclasses import dataclass
from uuid import UUID


class Command:
    pass


@dataclass(slots=True, frozen=True, eq=True)
class CreateUser(Command):
    name: str
    age: int
    gender: str
    school: str
    phone: str
    description: str
    email: str
    photo: str
    job: str


@dataclass(slots=True, frozen=True, eq=True)
class LikeUser(Command):
    user_id: UUID
    liked_user_id: UUID
