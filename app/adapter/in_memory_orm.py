from collections import deque
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, MetaData, String, Table, TypeDecorator, event, func
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import registry, relationship

from app.domain import models
from app.domain.enums import Gender

metadata = MetaData()
mapper_registry = registry(metadata=metadata)


class GUID(TypeDecorator):
    impl = String
    cache_ok = False

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(String)

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        else:
            return "%s" % str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return str(value)


class TimeStamp(TypeDecorator):
    impl = DateTime
    LOCAL_TIMEZONE = datetime.utcnow().astimezone().tzinfo
    cache_ok = False

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if value.tzinfo is None:
            value = value.astimezone(self.LOCAL_TIMEZONE)

        return value.astimezone(timezone.utc)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)


# table difinition
users = Table(
    "tinder_clone_users",  # Table names
    mapper_registry.metadata,
    Column("id", GUID, primary_key=True),
    Column("create_dt", TimeStamp(), default=func.now(), server_default=func.now()),
    Column("update_dt", TimeStamp(), default=func.now(), onupdate=func.current_timestamp(), server_default=func.now()),
    Column("name", String),
    Column("age", Integer),
    Column("gender", String),
    Column("job", String),
    Column("phone", String),
    Column("email", String),
    Column("photo", sqlite.JSON),
    Column("description", String),
)

likes = Table(
    "tinder_clone_likes",
    mapper_registry.metadata,
    Column("user_id", GUID, ForeignKey(users.name + ".id")),
    Column("liked_user_id", GUID, ForeignKey(users.name + ".id")),
    Column("disliked_user_id", GUID, ForeignKey(users.name + ".id")),
)


def start_mappers():
    mapper_registry.map_imperatively(
        models.User,
        users,
        properties={
            "users_liked_by_self": relationship(
                models.User,
                secondary=likes,
                primaryjoin="models.User.id == tinder_clone_likes.c.user_id",
                secondaryjoin="models.User.id == tinder_clone_likes.c.liked_user_id",
                back_populates="users_who_like_self",
                collection_class=set,
                lazy="selectin",
            ),
            "users_who_like_self": relationship(
                models.User,
                secondary=likes,
                primaryjoin="models.User.id == tinder_clone_likes.c.liked_user_id",
                secondaryjoin="models.User.id == tinder_clone_likes.c.user_id",
                back_populates="users_liked_by_self",
                collection_class=set,
                lazy="selectin",
            ),
            "users_disliked_by_self": relationship(
                models.User,
                secondary=likes,
                primaryjoin="models.User.id == tinder_clone_likes.c.user_id",
                secondaryjoin="models.User.id == tinder_clone_likes.c.disliked_user_id",
                back_populates="users_who_dislike_self",
                collection_class=set,
            ),
            "users_who_dislike_self": relationship(
                models.User,
                secondary=likes,
                primaryjoin="models.User.id == tinder_clone_likes.c.disliked_user_id",
                secondaryjoin="models.User.id == tinder_clone_likes.c.user_id",
                back_populates="users_disliked_by_self",
                collection_class=set,
            ),
        },
        eager_defaults=True,
    )


@event.listens_for(models.User, "load")
def receive_load_user_application_queue(user: models.User, _):
    user.events = deque()
