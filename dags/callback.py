import logging
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, get_current_context
from airflow.utils.trigger_rule import TriggerRule
from airflow.models.dagrun import DagRun

from args import default_args


def task_failure_alert(context):
    logging.info("Context --> %s", context)


def get_failed_upstream_task(ti):
    dag_run: DagRun = get_current_context().get("dag_run")

    # get tasks is the direct relatives. True - for upstream
    upstream_task_ids = {t.task_id for t in ti.task.get_direct_relatives(True)}

    # grab all of the failed task instance in the current run
    # which will get us tasks that some of might be un-related to this one
    failed_task_instances = dag_run.get_task_instances(state="failed")

    failed_upstream_task_ids = [
        failed_task.task_id
        for failed_task in failed_task_instances
        if failed_task.task_id in upstream_task_ids
    ]

    for failed_task_id in failed_upstream_task_ids:
        logging.info(f'The task "{failed_task_id}" has failed')


with DAG(dag_id="example_callback", default_args=default_args, catchup=False):
    task_a = BashOperator(
        task_id="task_a",
        bash_command="echos task_a",  # Wrong syntax
        on_failure_callback=task_failure_alert,
    )
    task_b = BashOperator(
        task_id="task_b",
        bash_command="echo task_b",
        on_failure_callback=task_failure_alert,
    )
    task_c = BashOperator(
        task_id="task_c",
        bash_command="echos task_c",  # Wrong syntax
        on_failure_callback=task_failure_alert,
    )

    report_failed_task = PythonOperator(
        task_id="report_failed_task",
        python_callable=get_failed_upstream_task,
        trigger_rule=TriggerRule.ALL_DONE,
    )

    task_a >> report_failed_task
    task_b >> report_failed_task
    task_c >> report_failed_task
