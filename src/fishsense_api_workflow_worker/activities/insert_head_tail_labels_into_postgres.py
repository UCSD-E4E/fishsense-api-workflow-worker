"""Activity to insert head-tail labels into PostgreSQL database."""

from typing import List

from sqlmodel.ext.asyncio.session import AsyncSession
from temporalio import activity

from fishsense_api_workflow_worker.database import Database
from fishsense_api_workflow_worker.models.head_tail_label import HeadTailLabel


@activity.defn
async def insert_head_tail_labels_into_postgres(labels: List[HeadTailLabel]):
    # pylint: disable=duplicate-code
    """Activity to insert head-tail labels into PostgreSQL database."""

    database = Database()
    async with AsyncSession(database.engine) as conn:
        for label in labels:
            if activity.is_cancelled():
                await conn.rollback()
                return

            existing_label = await database.select_head_tail_labels_by_task_id(
                label.label_studio_task_id
            )
            if existing_label:
                label.id = existing_label.id

            await database.insert_or_update_head_tail_label(label, session=conn)

        await conn.commit()
