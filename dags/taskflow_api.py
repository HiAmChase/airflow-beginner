from airflow.decorators import dag, task
from datetime import datetime
from args import default_args


@dag(
    dag_id="taskflow_api",
    default_args=default_args,
    start_date=datetime(2023, 10, 9),
    schedule_interval="@daily",
    catchup=False
)
def hello_world_etl():

    @task(multiple_outputs=True)
    def get_name():
        return {
            "first_name": "Ngoc",
            "last_name": "Thinh"
        }

    @task()
    def get_age():
        return 22

    @task()
    def greet(first_name, last_name, age):
        print(
            f"Hello World! My name is {first_name} {last_name}, and I am {age} years old!")

    name_dict = get_name()
    age = get_age()
    greet(
        first_name=name_dict["first_name"],
        last_name=name_dict["last_name"],
        age=age
    )


greet_dag = hello_world_etl()
