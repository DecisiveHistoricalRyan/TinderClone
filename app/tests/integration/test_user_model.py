from uuid import uuid4

import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.domain.enums import Gender
from app.domain.models import User

my_faker = Faker()


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession):
    id = uuid4()
    # GIVEN
    user = User(
        id=id,
        name="Migo",
        age=32,
        gender=Gender.Male.value,
        school="KNSU",
        phone="010-0000-0000",
        description="This is me",
        email="saka90030@gmail.com",
        photo=[my_faker.url()],
        job="programmer",
    )
    session.add(user)
    await session.commit()

    # WHEN
    q = await session.execute(select(User))
    us: User = q.scalars().first()

    # THEN
    assert us is not None
    assert us.id == str(id)
