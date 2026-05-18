from datetime import datetime
import sys

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

sys.path.append("/opt/airflow/src")

from weather_pipeline.extract import WeatherExtractor


def extract_weather_data():
    extractor = WeatherExtractor()

    data = extractor.extract(
        location="Lagos,Nigeria",
        start_date="2026-05-01",
        end_date="2026-05-03",
    )

    print(data)


with DAG(
    dag_id="weather_extract_only",
    start_date=datetime(2026, 5, 18),
    schedule=None,
    catchup=False,
    tags=["weather", "extract"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_weather_data",
        python_callable=extract_weather_data,
    )
