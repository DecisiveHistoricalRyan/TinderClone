import starlette.status
from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse

from app.domain import commands
from app.entrypoints import deps
from app.service_layer import handlers
from app.service_layer.unit_of_work import AbstractUnitOfWork

from .schemas import UserIn

router = APIRouter()


@router.get("/ping")
def health():
    return "pong"


@router.post(
    "/users",
    response_class=PlainTextResponse,
    status_code=starlette.status.HTTP_201_CREATED,
)
async def create_user(
    create_data: UserIn,
    uow: AbstractUnitOfWork = Depends(deps.get_uow),
):
    try:
        create_user_command = commands.CreateUser(**create_data.dict())
        await handlers.create_user(msg=create_user_command, uow=uow)
    except Exception:
        raise
    else:
        return "user created!"
