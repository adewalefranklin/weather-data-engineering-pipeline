from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def test_airflow_connection():
    print("Airflow can run Python code successfully.")


with DAG(
    dag_id="weather_pipeline_orchestration",
    start_date=datetime(2026, 5, 18),
    schedule=None,
    catchup=False,
    tags=["weather", "portfolio"],
) as dag:

    test_task = PythonOperator(
        task_id="test_airflow_connection",
        python_callable=test_airflow_connection,
    )