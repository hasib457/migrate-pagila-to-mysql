# pylint:  disable-all
import os
from datetime import datetime, timedelta

from operators import (
    DataQualityOperator,
    CreateMySqlTableOperator,
    PostgresToMySqlOperator
)

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from helpers import SqlQueries


# dictionary that maps table names to their "last_update" column names and creation query
tables = {
    "actor": ["last_update", SqlQueries.create_actor],
    "address": ["last_update", SqlQueries.create_address],
    "category": ["last_update", SqlQueries.create_category],
    "city": ["last_update", SqlQueries.create_city],
    "country": ["last_update", SqlQueries.create_country],
    "customer": ["last_update", SqlQueries.create_customer],
    "film": ["last_update", SqlQueries.create_film],
    "film_actor": ["last_update", SqlQueries.create_film_actor],
    "film_category": ["last_update", SqlQueries.create_film_category],
    "inventory": ["last_update", SqlQueries.create_inventory],
    "language": ["last_update", SqlQueries.create_language],
    "payment": ["payment_date", SqlQueries.create_payment],
    "rental": ["last_update", SqlQueries.create_rental],
    "staff": ["last_update", SqlQueries.create_staff],
    "store": ["last_update", SqlQueries.create_store],
}

default_args = {
    "owner": "Hassib",
    "description": "Migrate pagila data from postgres to mysql",
    "start_date": datetime(2023, 10, 31),
    "schedule_interval": "0 0 * * *",
    "catchup": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "email_on_retry": False,
}

dag = DAG(
    "Migrate_pagila_from_postgres_to_mysql",
    default_args=default_args,
)

start_operator = EmptyOperator(task_id="Begin_execution", dag=dag)


create_db_database = CreateMySqlTableOperator(
    task_id="create_db_database", dag=dag, mysql_conn_id="mysql", sql=SqlQueries.create_db_database,
)

# List to store creation, migration and quality check tasks
creation_tasks, migration_tasks, quality_checks = [], [], []

# Iterate through table names and create migration tasks
for table_name, [last_update, create_query] in tables.items():
    # create create table task
    create_task = CreateMySqlTableOperator(
        task_id=f"create_{table_name}_table", dag=dag, mysql_conn_id="mysql", sql=create_query,
    )
    creation_tasks.append(create_task)

    # Create migration task
    migration_task = PostgresToMySqlOperator(
        task_id=f"migrate_{table_name}",
        postgres_conn_id="postgres",  # PostgreSQL connection
        mysql_conn_id="mysql",  # MySQL connection
        pg_selection_query=SqlQueries.select_statement.format(table_name, last_update, "{}"),
        mysql_insertion_query=SqlQueries.insert_statement.format(table_name, "{}"),
        last_update_query=SqlQueries.last_update.format(last_update, table_name),
        table=table_name,
        mysql_db= 'db',
        insert_mode="truncate",
        dag=dag,
    )
    migration_tasks.append(migration_task)

    # Create quality check task
    quality_check = DataQualityOperator(
        task_id=f"data_quality_check_{table_name}",
        dag=dag,
        dq_checks=[
            {
                "test_sql": f"SELECT COUNT(*) FROM db.{table_name} WHERE {last_update} IS NULL",
                "expected_result": 0,
                "comparison": "=",  # Check for NULL values in the last_update column
            },
            {
                "test_sql": f"SELECT COUNT(*) FROM db.{table_name}",
                "expected_result": 0,
                "comparison": ">",
            },
        ],
        mysql_conn_id="mysql",
    )
    quality_checks.append(quality_check)



end_operator = EmptyOperator(task_id="Stop_execution", dag=dag)


for i in range(len(tables)):
    start_operator >> create_db_database >> creation_tasks[i] >> migration_tasks[i] >> quality_checks[i] >> end_operator
