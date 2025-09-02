import logging
from typing import List

from label_studio_sdk.client import LabelStudio
from temporalio import activity

from fishsense_api_workflow_worker.models.user import User

@activity.defn
async def collect_label_studio_users(label_studio_host: str, label_studio_api_key: str) -> List[User]:
    client = LabelStudio(base_url=label_studio_host, api_key=label_studio_api_key)
    users = client.users.list()
    return [User.from_label_studio(user) for user in users]