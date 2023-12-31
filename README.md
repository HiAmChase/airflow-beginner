<center><h1>Airflow Beginner</h1></center>

This document refer to Airflow Tutorial for Beginners - Full Course in 2 Hours 2022: [link](https://www.youtube.com/watch?v=K9AnJ9_ZAXE)

## I. Introduction

Apache Airflow is an open-source platform for developing, scheduling, and monitoring batch-oriented workflows. Airflow’s extensible Python framework enables you to build workflows connecting with virtually any technology

Airflow Documentation: [link](https://airflow.apache.org/docs/)

## II. Concepts

### 1. DAG & Tasks

A DAG – or a Directed Acyclic Graph – is a collection of all the tasks you want to run, organized in a way that reflects their relationships and dependencies.

A Task defines a unit of work within a DAG; it is represented as a node in the DAG graph

Example for DAG and tasks:

```python
with DAG('my_dag', start_date=datetime(2016, 1, 1)) as dag:
    task_1 = DummyOperator('task_1')
    task_2 = DummyOperator('task_2')
    task_1 >> task_2    # Define dependencies
```

The <em>task_1</em> is upstream of <em>task_2</em>, and conversely <em>task_2</em> is downstream of <em>task_1</em>. When a DAG Run is created, <em>task_1</em> will start running and <em>task_2</em> waits for <em>task_1</em> to complete successfully before it may start.

### 2. Task Lifecycle

A task goes through various stages from start to completion. In the Airflow UI (graph and tree views), these stages are displayed by a color representing each stage:

![Task Lifecycle](/images/task_lifecycle_diagram.png)

The happy flow consists of the following stages:

1. No status - scheduler created empty task instance

2. Scheduled - scheduler determined task instance needs to run

3. Queued - scheduler sent task to executor to run on the queue

4. Running - worker picked up a task and is now running it

5. Success - task completed

### 3. Operators

While DAGs describe how to run a workflow, `Operators` determine what actually gets done by a task.

- BashOperator - executes a bash command

- PythonOperator - calls an arbitrary Python function

- EmailOperator - sends an email

- SimpleHttpOperator - sends an HTTP request

- MySqlOperator, SqliteOperator, PostgresOperator, MsSqlOperator, OracleOperator, JdbcOperator, etc. - executes a SQL command

- Sensor - an Operator that waits (polls) for a certain time, file, database row, S3 key, etc…

### 4. Catchup & Backfill

Document for Airflow Catchup & Backfill: [link](https://medium.com/nerd-for-tech/airflow-catchup-backfill-demystified-355def1b6f92)

**a. Start Date & Execution Date**

<em>start_date</em> - date at which DAG will start being scheduled

<em>schedule_interval</em> - the interval of time from the minimum start_date at which we want our DAG to be triggered

![Catchup & Backfill](/images/catchup_backfill.webp)

```
Trigger Point → start_date + { schedule_interval } → till the end.
```

**b. Catchup**

Catchup refers to the process of scheduling and executing all the past DAG runs that would have been scheduled if the DAG had been created and running at an earlier point in time

![Catchup](/images/catchup.png)

**c. Backfill**

Backfill command will re-run all the instances of the <em>dag_id</em> for all the intervals within the specified start and end date. It is also possible to re-run specific tasks within a dag.

This can be done through CLI. Run the below command

```
airflow dags backfill \
    --start-date START_DATE \
    --end-date END_DATE \
    dag_id
```

### 5. Data Sharing With XCOM

XComs are a mechanism that let Tasks talk to each other, as by default Tasks are entirely isolated and may be running on entirely different machines.

```python
# Push value to XCOM
task_instance.xcom_push(key="age", value=22)

# Pulls the return_value XCOM from "pushing_task"
value = xcom_pull(task_ids="task_id", key="age")
```

### 6. Schedule with Cron Expression

Each DAG may or may not have a schedule, which informs how DAG Runs are created. <em>schedule_interval</em> is defined as a DAG arguments, and receives preferably a cron expression as a str, or a datetime.timedelta object.

You can use one of these cron “preset”:

| Preset     | Meaning                                                         | Cron            |
| ---------- | --------------------------------------------------------------- | --------------- |
| `None`     | Don’t schedule, use for exclusively “externally triggered” DAGs |
| `@once`    | Schedule once and only once                                     |
| `@hourly`  | Run once an hour at the beginning of the hour                   | `0 \* \* \* \*` |
| `@daily`   | Run once a day at midnight                                      | `0 0 \* \* \*`  |
| `@weekly`  | Run once a week at midnight on Sunday morning                   | `0 0 \* \* 0`   |
| `@monthly` | Run once a month at midnight of the first day of the month      | `0 0 1 \* \*`   |
| `@yearly`  | Run once a year at midnight of January 1                        | `0 0 1 1 \*`    |

To generate specific cron: [Crontab](https://crontab.guru/)

### 7. Trigger Rules

By default, Airflow will wait for all the parent/upstream tasks for **successful** completion before it runs that task. However, this is just the default behavior of the Airflow, and you can control it using the `trigger_rule` the argument to a Task.

The options for trigger_rule are:

- all_success
- all_failed
- all_done
- one_failed
- one_success
- none_failed

**a. all_success**

- This is the default trigger
- Triggered when parents/upstream tasks succeed

**b. all_failed**

- Triggered when all parents/upstream tasks are in a failed or upstream_failed state
- Used when you want to do cleaning or something more complex to skip callback.

**c. all_done**

- Triggered when all parents/upstream tasks executed
- **It doesn’t depend upon their state of execution (failure, skip, success)**
- Used for the task that we always want to execute

**d. one_failed**

- Triggered as soon as at least one parent/upstream task failed
- It does not wait for the execution of all parents
- Used for long tasks and wants to execute other task if one fails

**e. one_success**

- Triggered as soon as at least one parent/upstream task gets succeeds
- It does not wait for the execution of all parents

**f. none_failed**

- Triggered if parents haven’t failed (i.e. all succeeded or skipped)
- Used to handle the skipped status.

<em>More Documentation about Trigger Rules: [link](https://medium.com/@knoldus/triggers-in-apache-airflow-30190d50fa5e)</em>
�