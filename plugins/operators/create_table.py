# pylint:  disable-all

import logging

from airflow.models import BaseOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook


class CreateMySqlTableOperator(BaseOperator):
    """
    Operator that creates a Mysql table by executing a SQL statement.

    :param mysql_conn_id: The connection ID for mysql.
    :type mysql_conn_id: str
    :param sql: The SQL statement to execute for creating a table.
    """

    ui_color = "#C98066"

    def __init__(
        self,
        mysql_conn_id: str = "mysql",
        sql: str = "",
        *args,
        **kwargs,
    ):

        super().__init__(*args, **kwargs)
        self.mysql_conn_id = mysql_conn_id
        self.sql = sql

    def execute(self, context):
        mysql_hook = MySqlHook(self.mysql_conn_id)
        try:
            mysql_hook.run(self.sql)
            logging.info(f"Table {self.sql} created successfully in mysql.")

        except Exception as e:
            raise ValueError(
                f"Failed to create table: {e} "
            )
