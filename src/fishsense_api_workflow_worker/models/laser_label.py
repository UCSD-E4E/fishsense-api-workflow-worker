"""Model representing a laser label from Label Studio."""

import logging
from typing import Any
from urllib.parse import urlparse

from pydantic import BaseModel


class LaserLabel(BaseModel):
    """Model representing a laser label from Label Studio."""

    task_id: int
    checksum: str
    x: int
    y: int

    @classmethod
    def from_task(cls, task: Any) -> "LaserLabel":
        """Create a LaserLabel instance from a Label Studio task."""

        log = logging.getLogger("LaserLabel")
        log.debug("Initializing LaserLabel with task ID: %s", task.id)

        return cls(
            task_id=task.id,
            checksum=cls.__parse_checksum(task),
            x=cls.__parse_x_y(task)[0],
            y=cls.__parse_x_y(task)[1],
        )

    @staticmethod
    def __parse_checksum(task: Any) -> str:
        log = logging.getLogger("LaserLabel")
        checksum = urlparse(task.data["img"]).path.split("/")[-1]

        log.debug("Parsed checksum: %s", checksum)

        return checksum

    @staticmethod
    def __parse_x_y(task: Any) -> tuple[int, int]:
        log = logging.getLogger("LaserLabel")
        original_width = task.annotations[0]["result"][0]["original_width"]
        original_height = task.annotations[0]["result"][0]["original_height"]

        log.debug(
            "Parsed original height and width: %s, %s", original_width, original_height
        )

        x = int(round(task.annotations[0]["result"][0]["value"]["x"] * original_width))
        y = int(round(task.annotations[0]["result"][0]["value"]["y"] * original_height))

        log.debug("Parsed coordinates: x=%s, y=%s", x, y)

        return x, y
