from datetime import datetime
import sys

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator

sys.path.append("/opt/airflow/src")

from weather_pipeline.pipeline import WeatherPipeline


def run_weather_pipeline():

    pipeline = WeatherPipeline()

    pipeline.run(
        locations=[
            {"city": "Lagos", "country": "Nigeria"}
        ],
        start_date="2026-05-01",
        end_date="2026-05-03",
    )


with DAG(
    dag_id="weather_pipeline_with_glue",
    start_date=datetime(2026, 5, 18),
    schedule=None,
    catchup=False,
    tags=["weather", "glue", "spark"],
) as dag:

    # TASK 1 — Extract + Load raw JSON to S3
    extract_and_load_task = PythonOperator(
        task_id="extract_and_load_weather_data",
        python_callable=run_weather_pipeline,
    )

    # TASK 2 — Trigger Glue Spark transformation
    run_glue_transform = GlueJobOperator(
        task_id="run_glue_weather_transform",
        job_name="Weather ETL Spark Transformation",
        aws_conn_id="aws_default",
        region_name="us-east-1",
        iam_role_name="AWSGlueServiceRole-practice",
        script_location="s3://aws-glue-assets-972775291781-us-east-1/scripts/Weather ETL Spark Transformation.py",
        script_args={
            "--RAW_PATH": "s3://revised-weather-pipeline/raw/weather/",
            "--OUTPUT_PATH": "s3://revised-weather-pipeline/transformed/weather/",
        },
        wait_for_completion=True,
    )

    # Task dependency
    extract_and_load_task >> run_glue_transform