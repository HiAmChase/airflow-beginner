from airflow import DAG
from airflow.operators.email import EmailOperator

from args import default_args

with DAG(dag_id="send_email", default_args=default_args, catchup=False):
    send_email = EmailOperator(
        task_id="send_email_task",
        to="ngocthinh303@gmail.com",
        subject="Airflow Alert",
        html_content=""" <h3>Email Test</h3> """,
    )

    send_email
