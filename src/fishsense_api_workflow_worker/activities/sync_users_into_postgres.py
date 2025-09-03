"""Activity to sync users from Label Studio to Postgres database."""

from typing import List

from label_studio_sdk.client import LabelStudio
from sqlmodel.ext.asyncio.session import AsyncSession
from temporalio import activity

from fishsense_api_workflow_worker.database import Database
from fishsense_api_workflow_worker.models.user import User


@activity.defn
async def sync_users_into_postgres(
    label_studio_host: str, label_studio_api_key: str, database_url: str
):
    """Synchronize users from Label Studio to the local Postgres database."""

    client = LabelStudio(
        base_url=f"https://{label_studio_host}", api_key=label_studio_api_key
    )
    users = client.users.list()

    database = Database(database_url)
    async with AsyncSession(database.engine) as conn:
        for user in [User.from_label_studio(user) for user in users]:
            if activity.is_cancelled():
                await conn.rollback()
                return

            existing_user = await database.select_user_by_email(user.email)
            if existing_user:
                user.id = existing_user.id

            await database.insert_or_update_user(user, session=conn)

        await conn.commit()
