"""Model representing a user."""

from datetime import datetime

from sqlmodel import Field, SQLModel
import pytz


class User(SQLModel, table=True):
    """Model representing a user."""

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(max_length=100, unique=True)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    last_activity: datetime | None = Field(default=None)
    date_joined: datetime | None = Field(default=None)

    @classmethod
    def from_label_studio(cls, user) -> "User":
        """Create a User instance from a Label Studio user."""

        from label_studio_sdk import (  # pylint: disable=import-outside-toplevel
            LseUserApi,
        )

        user: LseUserApi = user

        los_angeles = pytz.timezone("America/Los_Angeles")

        last_activity = los_angeles.localize(user.last_activity) if user.last_activity else None
        date_joined = los_angeles.localize(user.date_joined) if user.date_joined else None

        return cls(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            last_activity=last_activity,
            date_joined=date_joined,
        )
