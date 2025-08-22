import logging
from datetime import timedelta
from typing import List

from temporalio import workflow

from fishsense_api_workflow_worker.models.head_tail_label import HeadTailLabel


@workflow.defn
class ReadLabelStudioHeadTailLabelsWorkflow:
    def __init__(self):
        self.__log = logging.getLogger("ReadLabelStudioHeadTailLabelsWorkflow")

    @workflow.run
    async def run(
        self,
        label_studio_host: str,
        label_studio_api_key: str,
        head_tail_project_id: int,
    ):

        self.__log.debug("Label Studio server location: %s", label_studio_host)
        self.__log.info(
            "Preparing to read head-tail labels from Label Studio project: %s",
            head_tail_project_id,
        )

        head_tail_labels: List[HeadTailLabel] = await workflow.execute_activity(
            "collect_label_studio_head_tail_labels",
            args=(label_studio_host, label_studio_api_key, head_tail_project_id),
            schedule_to_close_timeout=timedelta(minutes=10),
        )

        return head_tail_labels
