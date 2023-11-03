from airflow.plugins_manager import AirflowPlugin
from operators.postgres_to_mysql import PostgresToMySqlOperator
from operators.data_quality import DataQualityOperator
from operators.create_table import CreateMySqlTableOperator
from helpers import SqlQueries
import helpers

class MyPlugin(AirflowPlugin):
    name = 'sylndr_plugin'
    operators = [PostgresToMySqlOperator, DataQualityOperator, CreateMySqlTableOperator]
    helpers = [helpers.SqlQueries]