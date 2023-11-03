# pylint:  disable-all

from airflow.models import BaseOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook


class DataQualityOperator(BaseOperator):
    """
    Performs data quality checks on a set of tables in mysql.

    :param dq_checks: List check statments for data quality
    :type dq_checks: list[str]
    :param mysql_conn_id: ID of the mysql connection to use
    :type mysql_conn_id: str
    """

    ui_color = "#89DA59"

    def __init__(
        self,
        dq_checks: list = [],
        mysql_conn_id: str = "mysql",
        *args,
        **kwargs,
    ):

        super().__init__(*args, **kwargs)
        # Map params
        self.mysql_conn_id = mysql_conn_id
        self.dq_checks = dq_checks

    def execute(self, context):
        mysql_hook = MySqlHook(self.mysql_conn_id)

        for i, dq_check in enumerate(self.dq_checks):
            test_sql = dq_check["test_sql"]
            expected_result = dq_check["expected_result"]
            comparison = dq_check.get("comparison", "=")

            try:
                records = mysql_hook.get_records(test_sql)
                result = records[0][0]

                if comparison == "=":
                    if result != expected_result:
                        raise ValueError(
                            f" Test query {test_sql} returned {result}, expected {expected_result}"
                        )
                elif comparison == ">":
                    if result <= expected_result:
                        raise ValueError(
                            f"Test query {test_sql} returned {result}, expected greater than {expected_result}"
                        )
                elif comparison == "<":
                    if result >= expected_result:
                        raise ValueError(
                            f"Test query {test_sql} returned {result}, expected less than {expected_result}"
                        )
                else:
                    raise ValueError(
                        f"Invalid comparison operator '{comparison}' for data quality check #{i}."
                    )
            except Exception as e:
                raise ValueError(f"Failed to apply quality check #{i}, {e}") 
