"""Activity to insert laser labels into PostgreSQL database."""

from typing import List

import psycopg
from psycopg.rows import dict_row
from temporalio import activity

from fishsense_api_workflow_worker.config import PG_CONN_STR
from fishsense_api_workflow_worker.models.laser_label import LaserLabel
from fishsense_api_workflow_worker.sql_utils import do_query


@activity.defn
async def insert_laser_labels_into_postgres(labels: List[LaserLabel]):
    """Activity to insert laser labels into PostgreSQL database."""

    with psycopg.connect(PG_CONN_STR, row_factory=dict_row) as con, con.cursor() as cur:
        for label in labels:
            if activity.is_cancelled():
                con.rollback()
                return

            do_query(
                path="sql/update_laser_by_cksum.sql",
                cur=cur,
                params={"cksum": label.checksum, "x": label.x, "y": label.y},
            )
