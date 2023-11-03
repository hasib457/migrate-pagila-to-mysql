# pylint:  disable-all

from datetime import datetime

from airflow.models import BaseOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
import logging

class PostgresToMySqlOperator(BaseOperator):

    """
    This operator copies data from a PostgreSQL database to a MySQL database.
    :param postgres_conn_id: The source PostgreSQL connection ID.
    :type postgres_conn_id: str
    :param mysql_conn_id: The destination MySQL connection ID.
    :type mysql_conn_id: str
    :param pg_selection_query: The query to select data from the PostgreSQL database.
    :type pg_selection_query: str
    :param mysql_insertion_query: The query to insert data into the MySQL database.
    :type mysql_insertion_query: str
    :param last_update_query: The query to get the last update time from the MySQL database.
    :type last_update_query: str
    :param table: The name of the table to copy data to.
    :type table: str
    :param mysql_db: The name of the database to copy data to.
    :type mysql_db: str
    :param insert_mode: The mode of insertion. Can be either 'append' or 'truncate'.
    :type insert_mode: str
    """

    ui_color = '#F98866'

    def __init__(self,
                postgres_conn_id: str = "potgres",
                mysql_conn_id: str ="mysql",
                pg_selection_query: str = "",
                mysql_insertion_query: str ="",
                last_update_query: str ="",
                table: str = "",
                mysql_db: str = "",
                insert_mode:str ="truncate",
                *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.postgres_conn_id = postgres_conn_id
        self.mysql_conn_id = mysql_conn_id
        self.pg_selection_query = pg_selection_query
        self.mysql_insertion_query = mysql_insertion_query
        self.last_update_query=last_update_query
        self.table= table
        self.mysql_db = mysql_db
        self.insert_mode=insert_mode

        if self.insert_mode not in ["append", "truncate"]:
            raise ValueError("Insert mode must be either 'append' or 'truncate'.")
        
    # convert datetime object to string        
    def convert_timestamp(self, timestamp):
        return timestamp.strftime("%Y-%m-%d %H:%M:%S") if isinstance(timestamp, datetime) else str(timestamp)
    
    def convert_boolean(self, value):
        return 1 if value == 'True' else (0 if value == 'False' else value)

    def execute(self, context):
        """
        Copies data from a PostgreSQL database to a MySQL database.
        """
        postgres_hook = PostgresHook(self.postgres_conn_id)
        mysql_hook = MySqlHook(self.mysql_conn_id)

        if self.insert_mode == "truncate":
            truncate_statement = f"TRUNCATE TABLE {self.mysql_db}.{self.table};"
            mysql_hook.run(truncate_statement, autocommit=True)
        
        try: 
            last_update  = mysql_hook.get_records(self.last_update_query)[0][0]
        except Exception as e:
                raise ValueError(e) 

        selection_statement = self.pg_selection_query.format(last_update)

        results = postgres_hook.get_records(selection_statement) 

        if results is not None:
            # convert datetime object to string, casting boolean values and Add timestamp to each row of data.
            run_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            for i, row in enumerate(results):
                results[i] = tuple(map(self.convert_timestamp, row) )
                results[i] = tuple(map(self.convert_boolean, results[i] ))
                results[i] += (run_timestamp,)
                                
            # Insert data into MySQL database.
            insert_statment = self.mysql_insertion_query.format(str(results)[1:-1]).replace("'None'", 'NULL')

            try:
                mysql_hook.run(insert_statment, autocommit=True)
                logging.info(f"Data inserted in {self.table} Table successfully in MYSQL.")
            except Exception as e:
                raise ValueError(f"Failed to insert data in the {self.table} table:  {e}") 
        else:
            logging.info(f"No data to insert in {self.table} Table.")

