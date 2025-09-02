from typing import List

from sqlmodel.ext.asyncio.session import AsyncSession
from temporalio import activity

from fishsense_api_workflow_worker.database import Database
from fishsense_api_workflow_worker.models.user import User


@activity.defn
async def insert_users_into_postgres(users: List[User]):
    database = Database()
    async with AsyncSession(database.engine) as conn:
        for user in users:
            if activity.is_cancelled():
                await conn.rollback()
                return

            existing_user = await database.select_user_by_email(user.email)
            if existing_user:
                user.id = existing_user.id

            await database.insert_or_update_user(user, session=conn)

        await conn.commit()
