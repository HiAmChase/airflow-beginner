from datetime import datetime

from airflow import DAG
from args import default_args
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

with DAG(
    dag_id="minio_s3",
    start_date=datetime(2023, 10, 11),
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False
) as dag:
    task_1 = S3KeySensor(
        task_id="sensor_minio_s3",
        bucket_name="airflow",
        bucket_key="company.csv",
        aws_conn_id="minio_conn",
        mode="poke",
        poke_interval=5,
        timeout=30
    )

    task_1
