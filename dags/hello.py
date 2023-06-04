from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
  "owner": "airflow",
  "start_date": datetime(2023, 6, 1),
  "email_on_failure": False,
  "email_on_retry": False,
  "email": "admin@localhost.com",
  "retries": 1, # it is going to retry a failed Task at least once.
  "retry_delay": timedelta(minutes=5)
}

with DAG("hello", schedule_interval=None, default_args=default_args, catchup=False) as dag:
  task1 = BashOperator(
    task_id = "task1",
    bash_command="sleep 5"
  )

  task1