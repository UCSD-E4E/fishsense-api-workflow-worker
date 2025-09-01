from __future__ import annotations

from typing import Iterable

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel, select, and_
from sqlmodel.ext.asyncio.session import AsyncSession

from fishsense_api_workflow_worker.config import settings
from fishsense_api_workflow_worker.models.camera import Camera
from fishsense_api_workflow_worker.models.dive import Dive
from fishsense_api_workflow_worker.models.image import Image


class Database:
    def __init__(self):
        self.engine = create_async_engine(self.__generate_database_url())

    def __generate_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{settings.postgres.username}:{settings.postgres.password}"
            + f"@{settings.postgres.host}:{settings.postgres.port}/{settings.postgres.database}"
        )

    async def init_database(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def insert_camera(self, camera: Camera):
        async with AsyncSession(self.engine) as session:
            session.add(camera)

            await session.commit()

    async def insert_dive(self, dive: Dive):
        async with AsyncSession(self.engine) as session:
            session.add(dive)

            await session.commit()

    async def insert_image(self, image: Image):
        async with AsyncSession(self.engine) as session:
            session.add(image)

            await session.commit()

    async def select_camera_by_serial_number(self, serial_number: str) -> Camera | None:
        async with AsyncSession(self.engine) as session:
            result = await session.exec(
                select(Camera).where(Camera.serial_number == serial_number)
            )

        return result.one_or_none()

    async def select_dive_by_id(self, dive_id: int) -> Dive | None:
        async with AsyncSession(self.engine) as session:
            result = await session.exec(select(Dive).where(Dive.id == dive_id))

        return result.one_or_none()

    async def select_dive_by_path(self, dive_path: str) -> Dive | None:
        async with AsyncSession(self.engine) as session:
            result = await session.exec(select(Dive).where(Dive.path == dive_path))

        return result.one_or_none()

    async def select_dives(self) -> Iterable[Dive]:
        async with AsyncSession(self.engine) as session:
            result = await session.exec(select(Dive).order_by(Dive.dive_datetime))

        return result.all()

    async def select_image_by_id(self, image_id: int) -> Image | None:
        async with AsyncSession(self.engine) as session:
            result = await session.exec(select(Image).where(Image.id == image_id))

        return result.one_or_none()

    async def select_image_by_checksum(self, image_checksum: str) -> Image | None:
        async with AsyncSession(self.engine) as session:
            result = await session.exec(
                select(Image).where(
                    and_(Image.checksum == image_checksum, Image.is_canonical == True)
                )
            )

        return result.one_or_none()

    async def select_image_by_dive(self, dive: Dive) -> Image | None:
        async with AsyncSession(self.engine) as session:
            result = await session.exec(
                select(Image).where(
                    and_(Image.dive_id == dive.id, Image.is_canonical == True)
                )
            )

        return result.one_or_none()

    async def select_image_by_path(self, path: str) -> Image | None:
        async with AsyncSession(self.engine) as session:
            result = await session.exec(select(Image).where(Image.path == path))

        return result.one_or_none()
