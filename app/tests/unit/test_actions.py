import random

import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain import commands
from app.domain.enums import Gender
from app.service_layer import handlers
from app.tests.fakes import FakeSqlUnitOfWork

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


# @pytest.mark.asyncio
# async def test_like_user(session):

#     cmd = commands.LikeUser(user_id=uuid4(), liked_user_id=uuid4())
#     uow = FakeSqlUnitOfWork(session)
#     await handlers.like_user(
#         msg=cmd,
#         uow=uow
#     )


@pytest.mark.asyncio
def test_see_matches():
    ...


@pytest.mark.asyncio
def test_get_users():
    ...


@pytest.mark.asyncio
def test_unmatches():
    ...
