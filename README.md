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
�