from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from args import default_args

with DAG(
    dag_id="bash_operator",
    description="This is first dag",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:
    task_1 = BashOperator(
        task_id="first_task", bash_command="echo hello work, this is first task"
    )

    task_2 = BashOperator(
        task_id="second_task",
        bash_command="echo hey, I am task 2 and will be running after task 1",
    )

    task_3 = BashOperator(
        task_id="third_task",
        bash_command="echo hey, I am task 3 and will be running afeter task 1 the same as task 2 ",
    )

    # Task dependencies method 1
    # task_1.set_downstream(task_2)
    # task_1.set_downstream(task_3)

    # Task dependencies method 2
    # task_1 >> task_2
    # task_1 >> task_3

    # Task dependencies method 3
    task_1 >> [task_2, task_3]
