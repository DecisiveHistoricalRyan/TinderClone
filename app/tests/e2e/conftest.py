import pytest_asyncio
from starlette.testclient import TestClient

from app.main import app


@pytest_asyncio.fixture(scope="function")
def user_id() -> str:
    return str(uuid.uuid4())


@pytest_asyncio.fixture(scope="function")
def user_name() -> str:
    return "Migo"


@pytest_asyncio.fixture(scope="function")
def user_age() -> int:
    return 32


@pytest_asyncio.fixture(scope="function")
def user_gender() -> str:
    return 'male'


@pytest_asyncio.fixture(scope="function")
def user_school() -> str:
    return "KNSU"


@pytest_asyncio.fixture(scope="function")
def user_phone() -> str:
    return "010-0000-0000"


@pytest_asyncio.fixture(scope="function")
def user_description() -> str:
    return "This is me"


@pytest_asyncio.fixture(scope="function")
def user_email() -> str:
    return "saka90030@gmail.com"


@pytest_asyncio.fixture(scope="function")
def user_photo() -> list[str]:
    return ["https://i.imgur.com/RefcteE.jpeg"]


@pytest_asyncio.fixture(scope="function")
def user_job() -> str:
    return "programmer"


@pytest_asyncio.fixture(scope="function")
async def user_data(
    user_name: str,
    user_age: int,
    user_gender: str,
    user_school: str,
    user_phone: str,
    user_description: str,
    user_email: str,
    user_photo: list[str],
    user_job: str,
):
    data = dict(
        name=user_name,
        age=user_age,
        gender=user_gender,
        school=user_school,
        phone=user_phone,
        description=user_description,
        email=user_email,
        photo=user_photo,
        job=user_job,
    )

    tc = TestClient(app)
    url = app.url_path_for('create_user')
    res = tc.post(
        url=url,
        json=data,
    )

    return data, res.status_code


