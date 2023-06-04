FROM apache/airflow:2.6.1-python3.10

ADD requirements.txt .
COPY config/airflow.cfg /opt/airflow/airflow.cfg
RUN pip install -r requirements.txt 