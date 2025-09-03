"""Workflow for reading head-tail labels from Label Studio."""

import logging
from datetime import timedelta
from typing import List

from temporalio import workflow

from fishsense_api_workflow_worker.models.head_tail_label import HeadTailLabel
from fishsense_api_workflow_worker.workflows.utils import sync_users


@workflow.defn
class ReadLabelStudioHeadTailLabelsWorkflow:
    # pylint: disable=too-few-public-methods
    """Workflow for reading head-tail labels from Label Studio."""

    def __init__(self):
        self.__log = logging.getLogger("ReadLabelStudioHeadTailLabelsWorkflow")

    @workflow.run
    async def run(
        self,
        label_studio_host: str,
        label_studio_api_key: str,
        database_url: str,
        head_tail_project_id: int,
    ):
        """Run the workflow to read head-tail labels."""

        self.__log.debug("Label Studio server location: %s", label_studio_host)
        self.__log.info(
            "Preparing to read head-tail labels from Label Studio project: %s",
            head_tail_project_id,
        )

        await sync_users(label_studio_host, label_studio_api_key, database_url)

        await workflow.execute_activity(
            "sync_label_studio_head_tail_labels",
            args=(
                label_studio_host,
                label_studio_api_key,
                database_url,
                head_tail_project_id,
            ),
            schedule_to_close_timeout=timedelta(minutes=20),
        )
