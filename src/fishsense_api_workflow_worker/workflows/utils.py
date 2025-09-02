"""Utility functions for workflows."""

from datetime import timedelta
from typing import List

from temporalio import workflow

from fishsense_api_workflow_worker.models.user import User


async def sync_users(label_studio_host: str, label_studio_api_key: str):
    """Synchronize users from Label Studio to the local Postgres database."""
    users: List[User] = await workflow.execute_activity(
        "collect_label_studio_users",
        args=(label_studio_host, label_studio_api_key),
        schedule_to_close_timeout=timedelta(minutes=10),
    )

    await workflow.execute_activity(
        "insert_users_into_postgres",
        args=(users,),
        schedule_to_close_timeout=timedelta(minutes=10),
    )
