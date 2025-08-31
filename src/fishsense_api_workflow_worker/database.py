from __future__ import annotations

from typing import Self

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from fishsense_api_workflow_worker.config import settings
from fishsense_api_workflow_worker.models.dive import Dive
from fishsense_api_workflow_worker.models.image import Image


class Database:
    def __init__(self):
        self.engine = create_async_engine(self.__generate_database_url())
        self.session = AsyncSession(self.engine)

    def __generate_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{settings.postgres.username}:{settings.postgres.password}"
            + f"@{settings.postgres.host}:{settings.postgres.port}/{settings.postgres.database}"
        )

    async def __aenter__(self) -> Self:
        await self.engine.begin()
        await self.session.begin()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()

        await self.session.close()
        await self.engine.dispose()

    async def select_dive_by_id(self, dive_id: int) -> Dive | None:
        result = await self.session.exec(select(Dive).where(Dive.id == dive_id))
        return result.one_or_none()

    async def select_dive_by_path(self, dive_path: str) -> Dive | None:
        result = await self.session.exec(select(Dive).where(Dive.path == dive_path))
        return result.one_or_none()

    async def select_image_by_id(self, image_id: int) -> Image | None:
        result = await self.session.exec(select(Image).where(Image.id == image_id))
        return result.one_or_none()

    async def select_image_by_checksum(self, image_checksum: str) -> Image | None:
        result = await self.session.exec(
            select(Image).where(
                Image.checksum == image_checksum and Image.is_canonical == True
            )
        )
        return result.one_or_none()

    async def select_image_by_dive(self, dive: Dive) -> Image | None:
        result = await self.session.exec(
            select(Image).where(Image.dive_id == dive.id and Image.is_canonical == True)
        )
        return result.one_or_none()
