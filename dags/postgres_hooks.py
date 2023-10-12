import csv
import logging
from datetime import datetime
from tempfile import NamedTemporaryFile

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from args import default_args


def postgres_to_s3():
    # step 1: query data from postgresql db and save into to text file
    hook = PostgresHook(postgres_conn_id="postgres_localhost")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("select * from orders where date <= '20220501'")
    with NamedTemporaryFile(mode="w", suffix="orders") as f:
    # with open("dags/get_orders.txt", "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(i[0] for i in cursor.description)
        csv_writer.writerows(cursor)
        cursor.close()
        conn.close()
        logging.info("Saved order data in text file get_orders.txt")

        # step 2: upload text file to s3
        s3_hook = S3Hook(aws_conn_id="minio_conn")
        s3_hook.load_file(
            filename=f.name,
            key="orders/get_orders.txt",
            bucket_name="airflow",
            replace=True
        )


with DAG(
    dag_id="postgres_hooks",
    default_args=default_args,
    start_date=datetime(2023, 10, 11),
    schedule_interval="@daily"
) as dag:
    task_1 = PythonOperator(
        task_id="postgres_to_s3",
        python_callable=postgres_to_s3
    )

    task_1
