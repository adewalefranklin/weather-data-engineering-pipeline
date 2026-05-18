from datetime import datetime
import sys

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

# Add src folder to Python path
sys.path.append("/opt/airflow/src")

from weather_pipeline.pipeline import WeatherPipeline


def run_weather_pipeline():

    pipeline = WeatherPipeline()

    pipeline.run(
        locations=[{"city": "Lagos", "country": "Nigeria"}],
        start_date="2026-05-01",
        end_date="2026-05-03",
    )


with DAG(
    dag_id="weather_pipeline_orchestration",
    start_date=datetime(2026, 5, 18),
    schedule=None,
    catchup=False,
    tags=["weather", "portfolio"],
) as dag:

    run_pipeline_task = PythonOperator(
        task_id="run_weather_pipeline",
        python_callable=run_weather_pipeline,
    )
