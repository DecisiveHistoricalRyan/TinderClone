from uuid import UUID

import pytest
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.selectable import Select

from app.domain.models import User


@pytest.mark.parametrize("user_id", [UUID("6882c47e-4355-4399-968a-c15f5a949e7e")])
@pytest.mark.asyncio
async def test_create_user(session: AsyncSession, user: User, user_id: UUID):
    session.add(user)
    await session.commit()

    # WHEN
    q = await session.execute(select(User))
    us: User = q.scalars().first()

    # THEN
    assert us is not None
    assert us.id == str(user_id)


@pytest.mark.asyncio
async def test_user_like_collection_feature(session: AsyncSession, two_users):
    """
    Test if a user presses a like button on a certain user,
    the like-pressed user can also see the user on 'users_who_like_self' collection
    """

    user, user2 = two_users
    session.add_all([user, user2])

    # GIVEN
    # user = create_user()
    # user2 = create_user()

    # session.add_all((user, user2))
    await session.commit()

    user.users_liked_by_self.add(user2)
    # user2.users_who_like_self.add(user1)
    await session.commit()

    # WHEN
    select_construct: Select = select(User)
    q: ChunkedIteratorResult = await session.execute(select_construct.where(User.id == user.id))

    us: User = q.scalars().first()

    # THEN

    assert user2 in us.users_liked_by_self
    assert user in user2.users_who_like_self


@pytest.mark.asyncio
async def test_user_dislike_collection_feature(session: AsyncSession, two_users):
    """
    Test if a user presses a dislike button on a certain user,
    the dislike-pressed user can also see the user on 'users_who_dislike_self' collection
    """
    user1, user2 = two_users
    # GIVEN
    session.add_all((user1, user2))
    await session.commit()

    user1.users_disliked_by_self.add(user2)
    # user2.users_who_like_self.add(user1)
    await session.commit()

    # WHEN
    select_construct: Select = select(User)
    q: ChunkedIteratorResult = await session.execute(select_construct.where(User.id == user1.id))

    us: User = q.scalars().first()

    # THEN
    assert user2 in us.users_disliked_by_self
    assert user1 in user2.users_who_dislike_self
