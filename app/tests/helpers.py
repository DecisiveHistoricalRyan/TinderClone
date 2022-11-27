import random
from uuid import uuid4

from faker import Faker

from app.domain import enums, models

my_faker = Faker()


def create_user():
    """
    Test For User Creation
    """
    id = uuid4()
    user = models.User(
        id=str(id),
        name=my_faker.name(),
        age=random.randint(19, 100),
        gender=enums.Gender.Male.value,
        school="KNSU",
        phone=my_faker.phone_number(),
        description=my_faker.sentence(),
        email=my_faker.email(),
        photo=[my_faker.image_url()],
        job=my_faker.job(),
    )
    return user
