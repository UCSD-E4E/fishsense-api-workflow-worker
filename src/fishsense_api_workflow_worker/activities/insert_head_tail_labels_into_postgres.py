"""Activity to insert head-tail labels into PostgreSQL database."""

from typing import List

import psycopg
from psycopg.rows import dict_row
from temporalio import activity

from fishsense_api_workflow_worker.config import PG_CONN_STR
from fishsense_api_workflow_worker.models.head_tail_label import HeadTailLabel
from fishsense_api_workflow_worker.sql_utils import do_query


@activity.defn
async def insert_head_tail_labels_into_postgres(labels: List[HeadTailLabel]):
    """Activity to insert head-tail labels into PostgreSQL database."""

    with psycopg.connect(PG_CONN_STR, row_factory=dict_row) as con, con.cursor() as cur:
        for label in labels:
            if activity.is_cancelled():
                con.rollback()
                return

            do_query(
                path="sql/update_headtail_labels.sql",
                cur=cur,
                params={
                    "cksum": label.checksum,
                    "head_x": label.head_x,
                    "head_y": label.head_y,
                    "tail_x": label.tail_x,
                    "tail_y": label.tail_y,
                },
            )
