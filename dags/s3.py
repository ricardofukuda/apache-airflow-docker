from airflow.providers.amazon.aws.operators.s3 import S3CreateBucketOperator, S3DeleteBucketOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow import DAG

default_args = {
  "owner": "airflow",
  "start_date": datetime(2023, 6, 1),
  "email_on_failure": False,
  "email_on_retry": False,
  "email": "admin@localhost.com",
  "retries": 1, # it is going to retry a failed Task at least once.
  "retry_delay": timedelta(minutes=5)
}

with DAG("s3", schedule_interval=None, default_args=default_args, catchup=False) as dag:
  createBucket = S3CreateBucketOperator(bucket_name = "airflow-test-1233456", aws_conn_id = "aws_conn", region_name="us-east-1")
  deleteBucket = S3DeleteBucketOperator(bucket_name = "airflow-test-1233456", aws_conn_id = "aws_conn", force_delete=True)

  sleep = BashOperator(
    task_id="sleep",
    bash_command="sleep 60"
  )

  createBucket >> sleep >> deleteBucket