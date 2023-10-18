from datetime import datetime

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

from args import default_args

with DAG(
    dag_id="postgres_operator",
    default_args=default_args,
    schedule_interval="0 0 * * *",
    catchup=False,
) as dag:
    task_1 = PostgresOperator(
        task_id="create_table",
        postgres_conn_id="postgres_localhost",
        sql="""
            create table if not exists dag_runs(
                dt date,
                dag_id character varying,
                primary key (dt, dag_id)
            )
        """,
    )
    task_2 = PostgresOperator(
        task_id="insert_table",
        postgres_conn_id="postgres_localhost",
        sql="""
            insert into dag_runs (dt, dag_id) values ('{{ ds }}', '{{ dag.dag_id }}');
        """,
    )
    task_3 = PostgresOperator(
        task_id="delete_data",
        postgres_conn_id="postgres_localhost",
        sql="""
            delete from dag_runs where dt = '{{ ds }}' and dag_id = '{{ dag.dag_id }}';
        """,
    )

    task_1 >> task_3 >> task_2
