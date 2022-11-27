import http
from dataclasses import asdict

import pytest
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import User


@pytest.mark.asyncio
async def test_create_user(user_data, session: AsyncSession):
    created_user_data, res = user_data
    assert res.status_code == http.HTTPStatus.CREATED

    q = await session.execute(select(User))
    user: User = q.scalars().first()
    assert user

    # for key, _ in created_user_data.items():
    #     assert created_user_data[key] ==
