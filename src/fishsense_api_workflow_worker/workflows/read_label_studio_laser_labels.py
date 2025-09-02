"""Workflow definition for reading laser labels from Label Studio."""

import logging
from datetime import timedelta
from typing import List

from temporalio import workflow

from fishsense_api_workflow_worker.models.laser_label import LaserLabel
from fishsense_api_workflow_worker.models.user import User


@workflow.defn
class ReadLabelStudioLaserLabelsWorkflow:
    # pylint: disable=too-few-public-methods
    """Workflow for reading laser labels from Label Studio."""

    def __init__(self):
        self.__log = logging.getLogger("ReadLabelStudioLaserLabelsWorkflow")

    @workflow.run
    async def run(
        self,
        label_studio_host: str,
        label_studio_api_key: str,
        laser_project_id: int,
    ):
        """Run the workflow to read laser labels."""

        self.__log.debug("Label Studio server location: %s", label_studio_host)
        self.__log.info(
            "Preparing to read laser labels from Label Studio project: %s",
            laser_project_id,
        )

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

        laser_labels: List[LaserLabel] = await workflow.execute_activity(
            "collect_label_studio_laser_labels",
            args=(label_studio_host, label_studio_api_key, laser_project_id),
            schedule_to_close_timeout=timedelta(minutes=10),
        )

        await workflow.execute_activity(
            "insert_laser_labels_into_postgres",
            args=(laser_labels,),
            schedule_to_close_timeout=timedelta(minutes=10),
        )
