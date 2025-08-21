"""Workflow definition for reading laser labels from Label Studio."""

import logging
from datetime import timedelta

from temporalio import workflow


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

        return await workflow.execute_activity(
            "read_label_studio_laser_labels",
            args=(label_studio_host, label_studio_api_key, laser_project_id),
            schedule_to_close_timeout=timedelta(minutes=10),
        )
