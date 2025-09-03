"""Utility functions for workflows."""

from datetime import timedelta

from temporalio import workflow


async def sync_users(
    label_studio_host: str, label_studio_api_key: str, database_url: str
):
    """Synchronize users from Label Studio to the local Postgres database."""

    await workflow.execute_activity(
        "sync_users_into_postgres",
        args=(label_studio_host, label_studio_api_key, database_url),
        schedule_to_close_timeout=timedelta(minutes=10),
    )
