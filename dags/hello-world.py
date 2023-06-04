from airflow import DAG
from textwrap import dedent
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
import json 
from airflow.operators.python import BranchPythonOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

default_args = {
  "owner": "airflow",
  "start_date": datetime(2023, 6, 1),
  "email_on_failure": False,
  "email_on_retry": False,
  "email": "admin@localhost.com",
  "retries": 1, # it is going to retry a failed Task at least once.
  "retry_delay": timedelta(minutes=5)
}


def _read_response(ti):
  val = ti.xcom_pull(
    task_ids='get_todos',
    key='return_value'
  )
  print(val)


def taskBranch(ti):
  val = ti.xcom_pull(
    task_ids='task1',
    key='return_value'
  )
  print(val)
  return "task4"

def _xcom_push():
  return "hello world!"

with DAG("hello_world", schedule_interval=None, default_args=default_args, catchup=True) as dag:
  get_todos = SimpleHttpOperator(
    task_id="get_todos",
    method="GET",
    endpoint="/todos",
    http_conn_id="jsonplaceholder", # should be configured using the Connections
    headers={"Content-Type": "application/json"}
  )

  read_response = PythonOperator( # read xcom
    task_id='read_response',
    python_callable=_read_response
  )

  print_date = BashOperator( # Uses jinja template and Variables
    task_id="print_date",
    bash_command="echo {{ ds }} && echo {{ var.value.my_message }}",
  )

  task1 = PythonOperator( # push xcom
    task_id="task1",
    python_callable=_xcom_push
  )

  task2 = BashOperator(
    task_id="task2",
    bash_command="sleep 8",
  )

  taskBranching = BranchPythonOperator( # Start branching execution flow
    task_id="taskBranching",
    python_callable=taskBranch
  )

  task3 = BashOperator(
    task_id="task3",
    bash_command="sleep 5"
  )

  task4 = BashOperator(
    task_id="task4",
    bash_command="sleep 5"
  )

  task5 = BashOperator(
    task_id="task5",
    bash_command="sleep 5",
    depends_on_past = False,
    trigger_rule = TriggerRule.ONE_SUCCESS
  )

  dag_run = TriggerDagRunOperator( # trigger another Dag
    task_id="triggerDagRun",
    trigger_dag_id = "hello",
    wait_for_completion = True,
    poke_interval = 5,
    allowed_states = "success"
  )

  print_date >> get_todos >> read_response >> [ task1, task2 ] >> taskBranching  >> [task3, task4] >> task5
