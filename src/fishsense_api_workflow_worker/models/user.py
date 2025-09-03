"""Model representing a user."""

from datetime import datetime

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """Model representing a user."""

    from label_studio_sdk import LseUserApi  # pylint: disable=import-outside-toplevel

    model_config = ConfigDict(ignored_types=(LseUserApi,))

    id: int = Field(default=None, primary_key=True)
    email: str = Field(max_length=100, unique=True)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    last_activity: datetime = Field(default=None)
    date_joined: datetime = Field(default=None)

    @classmethod
    def from_label_studio(cls, user: LseUserApi) -> "User":
        """Create a User instance from a Label Studio user."""

        return cls(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            last_activity=user.last_activity,
            date_joined=user.date_joined,
        )
