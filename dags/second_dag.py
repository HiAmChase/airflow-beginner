from airflow import DAG
from datetime import datetime

from airflow.operators.python import PythonOperator
from args import default_args


# MAX XCOM Size is 48kB
def greet(ti):
    first_name = ti.xcom_pull(task_ids="get_name", key="first_name")
    last_name = ti.xcom_pull(task_ids="get_name", key="last_name")
    age = ti.xcom_pull(task_ids="get_age", key="age")
    print(
        f"Hello World! My name is {first_name} {last_name}, and I am {age} years old!"
    )


def get_name(ti):
    ti.xcom_push(key="first_name", value="Ngoc")
    ti.xcom_push(key="last_name", value="Thinh")


def get_age(ti):
    ti.xcom_push(key="age", value=22)


with DAG(
    default_args=default_args,
    dag_id="python_operator",
    description="Second DAG using python operator",
    schedule_interval="@daily",
    catchup=False,
):
    task_1 = PythonOperator(
        task_id="greet",
        python_callable=greet,
    )

    task_2 = PythonOperator(task_id="get_name", python_callable=get_name)

    task_3 = PythonOperator(task_id="get_age", python_callable=get_age)

    [task_2, task_3] >> task_1
