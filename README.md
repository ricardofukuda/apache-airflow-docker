# Start the service
```
docker compose up --build
```

# For local development/test
**To install pip dependencies to use VisualCode autocomplete**
```
pipenv --python 3.10.6
pipenv install -r requirements.txt
pipenv shell
```

# Commands
**Info about the Airflow running:**
```
docker exec -it airflow-local-airflow-worker-1 bash
airflow info
```

**Print the list of active DAGs:**
```
airflow dags list
```

**Prints the list of tasks in the "hello_world" DAG:**
```
airflow tasks list hello_world
```

**Simple runtime test:**
```
python3 ./dags/hello-world.py
```

**Runs a single Task in test mode:**
```
airflow tasks test hello_world print_date 2023-05-01
```
OBS: Note that the airflow tasks test command runs task instances locally, outputs their log to stdout (on screen), does not bother with dependencies, and does not communicate state (running, success, failed, …) to the database. It simply allows testing a single task instance.

**Runs the DAG in test mode:**
```
airflow dags test hello_world 2023-05-01
```
OBS: The same applies to airflow dags test, but on a DAG level. It performs a single DAG run of the given DAG id. While it does take task dependencies into account, no state is registered in the database. It is convenient for locally testing a full run of your DAG, given that e.g. if one of your tasks expects data at some location, it is available.

**Backfill the DAG:**

Backfill will respect your dependencies, emit logs into files and talk to the database to record status.
```
airflow dags backfill hello_world --start-date 2023-05-01 --end-date 2023-05-03
```

**Starts a DAG:**

-e means execution_date
```
airflow dags trigger hello_world -e 2023-01-01
```

# Tips
If you want to use Airflow locally, your DAGs may try to connect to servers which are running on the host. In order to achieve that, an extra configuration must be added in docker-compose.yaml:
```
extra_hosts: - "host.docker.internal:host-gateway"
```
After that, use "host.docker.internal" instead of "localhost".

# Clean up
```
docker compose down --volumes --rmi all
```