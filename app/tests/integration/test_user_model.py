import random
from uuid import UUID, uuid4

import pytest
from faker import Faker
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.selectable import Select

from app.domain.enums import Gender
from app.domain.models import User

my_faker = Faker()


def create_user():
    id = uuid4()
    user = User(
        id=str(id),
        name=my_faker.name(),
        age=random.randint(19, 100),
        gender=Gender.Male.value,
        school="KNSU",
        phone=my_faker.phone_number(),
        description=my_faker.sentence(),
        email=my_faker.email(),
        photo=[my_faker.image_url()],
        job=my_faker.job(),
    )
    return user


@pytest.mark.parametrize("user_id", [UUID("6882c47e-4355-4399-968a-c15f5a949e7e")])
@pytest.mark.asyncio
async def test_create_user(session: AsyncSession, user: User, user_id: UUID):
    await session.commit()

    # WHEN
    q = await session.execute(select(User))
    us: User = q.scalars().first()

    # THEN
    assert us is not None
    assert us.id == str(user_id)


@pytest.mark.asyncio
async def test_user_like_collection_feature(session: AsyncSession):
    """
    Test if a user presses a like button on a certain user,
    the like-pressed user can also see the user on 'users_who_like_self' collection
    """

    # GIVEN
    user1 = create_user()
    user2 = create_user()

    session.add_all((user1, user2))
    await session.commit()

    user1.users_liked_by_self.append(user2)
    # user2.users_who_like_self.append(user1)
    await session.commit()

    # WHEN
    select_construct: Select = select(User)
    q: ChunkedIteratorResult = await session.execute(select_construct.where(User.id == user1.id))

    us: User = q.scalars().first()

    # THEN
    assert us.users_liked_by_self[0].id == user2.id
    assert us.users_liked_by_self[0].users_who_like_self[0].id == user1.id


@pytest.mark.asyncio
async def test_user_dislike_collection_feature(session: AsyncSession):
    """
    Test if a user presses a dislike button on a certain user,
    the dislike-pressed user can also see the user on 'users_who_dislike_self' collection
    """

    # GIVEN
    user1 = create_user()
    user2 = create_user()

    session.add_all((user1, user2))
    await session.commit()

    user1.users_disliked_by_self.append(user2)
    # user2.users_who_like_self.append(user1)
    await session.commit()

    # WHEN
    select_construct: Select = select(User)
    q: ChunkedIteratorResult = await session.execute(select_construct.where(User.id == user1.id))

    us: User = q.scalars().first()

    # THEN
    assert us.users_disliked_by_self[0].id == user2.id
    assert us.users_disliked_by_self[0].users_who_dislike_self[0].id == user1.id
