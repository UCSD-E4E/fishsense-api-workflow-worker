from datetime import datetime

from label_studio_sdk import LseUserApi
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str = Field(max_length=100, unique=True)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    last_activity: datetime = Field(default=None)
    date_joined: datetime = Field(default=None)

    @classmethod
    async def from_label_studio(cls, user: LseUserApi) -> "User":
        return cls(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            last_activity=user.last_activity,
            date_joined=user.date_joined,
        )
