from pydantic import BaseModel, Field


class UserIn(BaseModel):
    name: str = Field(..., title="name")
    age: int = Field(..., title="age")
    gender: str = Field(..., title="gender")
    phone: str = Field(..., title="phone")
    email: str = Field(..., title="email", description="this is description")
    photo: list = Field(..., title="photo")
    description: str = Field(..., title="description")
    school: str | None = Field(None, title="school")
    job: str | None = Field(None, title="job")
