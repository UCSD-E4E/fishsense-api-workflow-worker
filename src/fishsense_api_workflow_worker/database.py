from __future__ import annotations

import asyncio

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from fishsense_api_workflow_worker.config import settings
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

    async def insert_dive(self, dive: Dive):
        async with AsyncSession(self.engine) as session:
            session.add(dive)

            await session.commit()

    async def insert_image(self, image: Image):
        async with AsyncSession(self.engine) as session:
            session.add(image)

            await session.commit()

    async def select_dive_by_id(self, dive_id: int) -> Dive | None:
        async with AsyncSession(self.engine) as session:
            result = await session.exec(select(Dive).where(Dive.id == dive_id))

        return result.one_or_none()

    async def select_dive_by_path(self, dive_path: str) -> Dive | None:
        async with AsyncSession(self.engine) as session:
            result = await session.exec(select(Dive).where(Dive.path == dive_path))

        return result.one_or_none()

    async def select_image_by_id(self, image_id: int) -> Image | None:
        async with AsyncSession(self.engine) as session:
            result = await session.exec(select(Image).where(Image.id == image_id))

        return result.one_or_none()

    async def select_image_by_checksum(self, image_checksum: str) -> Image | None:
        async with AsyncSession(self.engine) as session:
            result = await session.exec(
                select(Image).where(
                    Image.checksum == image_checksum and Image.is_canonical == True
                )
            )

        return result.one_or_none()

    async def select_image_by_dive(self, dive: Dive) -> Image | None:
        async with AsyncSession(self.engine) as session:
            result = await session.exec(
                select(Image).where(
                    Image.dive_id == dive.id and Image.is_canonical == True
                )
            )

        return result.one_or_none()


__database = Database()
asyncio.run(__database.init_database())
