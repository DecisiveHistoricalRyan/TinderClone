import random
from uuid import uuid4

import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain import commands
from app.domain.enums import Gender
from app.service_layer import handlers

my_faker = Faker()


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession):
    cmd = commands.CreateUser(
        id=str(id),
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
    await handlers.create_user(cmd)

    q = await session.execute(
        """
        SELECT * FROM tinder_clone_users
        """
    )
    _ = q.scalars().first()


@pytest.mark.asyncio
async def test_like_user():

    cmd = commands.LikeUser(user_id=uuid4(), liked_user_id=uuid4())
    await handlers.like_user(
        msg=cmd,
    )


@pytest.mark.asyncio
def test_see_matches():
    ...


@pytest.mark.asyncio
def test_get_users():
    ...


@pytest.mark.asyncio
def test_unmatches():
    ...
