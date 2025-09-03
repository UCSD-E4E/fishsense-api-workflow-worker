"""Database interaction module for FishSense API Workflow Worker."""

from __future__ import annotations

from typing import Iterable

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel, and_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from fishsense_api_workflow_worker.models.camera import Camera
from fishsense_api_workflow_worker.models.dive import Dive
from fishsense_api_workflow_worker.models.head_tail_label import HeadTailLabel
from fishsense_api_workflow_worker.models.image import Image
from fishsense_api_workflow_worker.models.laser_label import LaserLabel
from fishsense_api_workflow_worker.models.user import User


class Database:
    """Database interaction class for FishSense API Workflow Worker."""

    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url)

    async def init_database(self) -> None:
        """Initialize the database by creating all tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def insert_or_update_camera(
        self, camera: Camera, session: AsyncSession | None = None
    ):
        """Insert or update (upsert) a camera in the database."""
        if session is not None:
            await session.merge(camera)
        else:
            async with AsyncSession(self.engine) as session:
                await session.merge(camera)

                await session.commit()

    async def insert_or_update_dive(
        self, dive: Dive, session: AsyncSession | None = None
    ):
        """Insert or update (upsert) a dive in the database."""
        if session is not None:
            await session.merge(dive)
        else:
            async with AsyncSession(self.engine) as session:
                await session.merge(dive)

                await session.commit()

    async def insert_or_update_head_tail_label(
        self, head_tail_label: HeadTailLabel, session: AsyncSession | None = None
    ):
        """Insert or update (upsert) a head-tail label in the database."""
        if session is not None:
            await session.merge(head_tail_label)
        else:
            async with AsyncSession(self.engine) as session:
                await session.merge(head_tail_label)

                await session.commit()

    async def insert_or_update_image(
        self, image: Image, session: AsyncSession | None = None
    ):
        """Insert or update (upsert) an image in the database."""
        if session is not None:
            await session.merge(image)
        else:
            async with AsyncSession(self.engine) as session:
                await session.merge(image)

                await session.commit()

    async def insert_or_update_laser_label(
        self, laser_label: LaserLabel, session: AsyncSession | None = None
    ):
        """Insert or update (upsert) a laser label in the database."""
        if session is not None:
            await session.merge(laser_label)
        else:
            async with AsyncSession(self.engine) as session:
                await session.merge(laser_label)

                await session.commit()

    async def insert_or_update_user(
        self, user: User, session: AsyncSession | None = None
    ):
        """Insert or update (upsert) a user in the database."""
        if session is not None:
            await session.merge(user)
        else:
            async with AsyncSession(self.engine) as session:
                await session.merge(user)

                await session.commit()

    async def select_camera_by_serial_number(self, serial_number: str) -> Camera | None:
        """Select a camera by its serial number."""
        async with AsyncSession(self.engine) as session:
            result = await session.exec(
                select(Camera).where(Camera.serial_number == serial_number)
            )

        return result.one_or_none()

    async def select_dive_by_path(self, dive_path: str) -> Dive | None:
        """Select a dive by its path."""
        async with AsyncSession(self.engine) as session:
            result = await session.exec(select(Dive).where(Dive.path == dive_path))

        return result.one_or_none()

    async def select_dives(self) -> Iterable[Dive]:
        """Select all dives ordered by dive datetime."""
        async with AsyncSession(self.engine) as session:
            result = await session.exec(select(Dive).order_by(Dive.dive_datetime))

        return result.all()

    async def select_head_tail_labels_by_task_id(
        self, task_id: int
    ) -> HeadTailLabel | None:
        """Select head-tail labels by their Label Studio task ID."""
        async with AsyncSession(self.engine) as session:
            result = await session.exec(
                select(HeadTailLabel).where(
                    HeadTailLabel.label_studio_task_id == task_id
                )
            )

        return result.one_or_none()

    async def select_image_by_checksum(self, image_checksum: str) -> Image | None:
        """Select a canonical image by its checksum."""
        async with AsyncSession(self.engine) as session:
            result = await session.exec(
                select(Image).where(
                    and_(Image.checksum == image_checksum, Image.is_canonical)
                )
            )

        return result.one_or_none()

    async def select_image_by_path(self, path: str) -> Image | None:
        """Select an image by its path."""
        async with AsyncSession(self.engine) as session:
            result = await session.exec(select(Image).where(Image.path == path))

        return result.one_or_none()

    async def select_laser_label_by_task_id(self, task_id: int) -> LaserLabel | None:
        """Select a laser label by its Label Studio task ID."""
        async with AsyncSession(self.engine) as session:
            result = await session.exec(
                select(LaserLabel).where(LaserLabel.label_studio_task_id == task_id)
            )

        return result.one_or_none()

    async def select_laser_labels(self) -> Iterable[LaserLabel]:
        """Select all laser labels."""
        async with AsyncSession(self.engine) as session:
            result = await session.exec(select(LaserLabel))

        return result.all()

    async def select_user_by_email(self, email: str) -> User | None:
        """Select a user by their email address."""
        async with AsyncSession(self.engine) as session:
            result = await session.exec(select(User).where(User.email == email))

        return result.one_or_none()
