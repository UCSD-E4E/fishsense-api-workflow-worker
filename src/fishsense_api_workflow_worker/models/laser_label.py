"""Model representing a laser label from Label Studio."""

import logging
from typing import Any
from urllib.parse import urlparse

from sqlmodel import Field, SQLModel


class LaserLabel(SQLModel, table=True):
    """Model representing a laser label from Label Studio."""

    id: int | None = Field(default=None, primary_key=True)
    label_studio_task_id: int | None = Field(default=None, unique=True, index=True)
    x: int | None = Field(default=None)
    y: int | None = Field(default=None)
    label: str | None = Field(default=None)

    image_id: int | None = Field(default=None, foreign_key="image.id")

    @classmethod
    async def from_task(cls, task: Any) -> "LaserLabel":
        """Create a LaserLabel instance from a Label Studio task."""

        log = logging.getLogger("LaserLabel")
        log.debug("Initializing LaserLabel with task ID: %s", task.id)

        checksum = cls.__parse_checksum(task)

        return cls(
            checksum,
            label_studio_task_id=task.id,
            x=cls.__parse_x_y(task)[0],
            y=cls.__parse_x_y(task)[1],
            label=cls.__parse_label(task),
        )

    @staticmethod
    def __parse_x_y(task: Any) -> tuple[int, int]:
        log = logging.getLogger("LaserLabel")
        original_width = task.annotations[0]["result"][0]["original_width"]
        original_height = task.annotations[0]["result"][0]["original_height"]

        log.debug(
            "Parsed original height and width: %s, %s", original_width, original_height
        )

        x = int(
            round(task.annotations[0]["result"][0]["value"]["x"] * original_width / 100)
        )
        y = int(
            round(
                task.annotations[0]["result"][0]["value"]["y"] * original_height / 100
            )
        )

        log.debug("Parsed coordinates: x=%s, y=%s", x, y)

        return x, y

    @staticmethod
    def __parse_label(task: Any) -> str:
        log = logging.getLogger("LaserLabel")
        label = task.annotations[0]["result"][0]["value"]["keypointlabels"][0]

        log.debug("Parsed label: %s", label)

        return label
