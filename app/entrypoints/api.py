
import starlette.status
from fastapi import APIRouter

from .schemas import UserIn

router = APIRouter()


@router.get('/ping')
def health():
    return 'pong'


@router.post(
    '/users',
    status_code=starlette.status.HTTP_201_CREATED,
)
def create_user(
    create_data: UserIn,
):
    try:
        pass
    except Exception:
        raise
