import random

import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain import commands
from app.domain.enums import Gender
from app.service_layer import handlers
from app.tests.fakes import FakeSqlUnitOfWork
from app.tests.helpers import create_user

my_faker = Faker()


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession):
    cmd = commands.CreateUser(
        name=my_faker.name(),
        age=random.randint(3, 20),
        gender=Gender.Male.value,
        school="KNSU",
        phone=my_faker.phone_number(),
        description=my_faker.sentence(),
        email=my_faker.email(),
        photo=[my_faker.image_url()],
        job=my_faker.job(),
    )
    uow = FakeSqlUnitOfWork(session)

    await handlers.create_user(cmd, uow=uow)

    q = await session.execute(
        """
        SELECT * FROM tinder_clone_users
        """
    )
    _ = q.scalars().first()


@pytest.mark.asyncio
async def test_like_user(session: AsyncSession):
    user1 = create_user()
    user2 = create_user()
    session.add_all((user1, user2))
    await session.commit()

    cmd = commands.LikeUser(user_id=user1.id, liked_user_id=user2.id)
    uow = FakeSqlUnitOfWork(session)

    await handlers.like_user(msg=cmd, uow=uow)
    user2_ = next(user for user in user1.users_liked_by_self)
    assert user2.id == user2_.id


@pytest.mark.asyncio
async def test_see_matches(session: AsyncSession):
    user1 = create_user()
    user2 = create_user()
    session.add_all((user1, user2))
    await session.commit()
    uow = FakeSqlUnitOfWork(session)

    cmd = commands.LikeUser(user_id=user1.id, liked_user_id=user2.id)
    await handlers.like_user(msg=cmd, uow=uow)

    cmd2 = commands.LikeUser(user_id=user2.id, liked_user_id=user1.id)
    is_matched = await handlers.like_user(msg=cmd2, uow=uow)

    assert is_matched


@pytest.mark.asyncio
async def test_get_users(session: AsyncSession):
    user1 = create_user()
    user2 = create_user()
    session.add_all((user1, user2))
    await session.commit()


@pytest.mark.asyncio
async def test_unmatches(session: AsyncSession):
    user1 = create_user()
    user2 = create_user()
    session.add_all((user1, user2))
    await session.commit()
