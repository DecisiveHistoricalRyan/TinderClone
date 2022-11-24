import asyncio
from typing import Coroutine

from app.domain import commands, models

from .exceptions import UserNotExist
from .unit_of_work import AbstractUnitOfWork


async def create_user(msg: commands.CreateUser, *, uow: AbstractUnitOfWork):
    async with uow:
        user = models.User.create_user(
            name=msg.name,
            age=msg.age,
            gender=msg.gender,
            phone=msg.phone,
            email=msg.email,
            photo=msg.photo,
            description=msg.description,
            school=msg.school,
        )
        uow.users.add(user)
        await uow.commit()


async def like_user(msg: commands.LikeUser, *, uow: AbstractUnitOfWork):
    async with uow:
        get_user_task: Coroutine = uow.users.get(msg.user_id)
        get_liked_user_task: Coroutine = uow.users.get(msg.liked_user_id)
        users: list[models.User] = await asyncio.gather(get_user_task, get_liked_user_task)
        user, liked_user = users
        if not all((user, liked_user)):
            raise UserNotExist(f"Users With Given User Ids Do Not Exist! ids:{msg.user_id},{msg.liked_user_id} ")

        user.users_liked_by_self.add(liked_user)
        matched = user in liked_user.users_who_like_self
        await uow.commit()

        return matched
