from datetime import datetime

from airflow import DAG
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator

with DAG(
    dag_id="glue_transform_only",
    start_date=datetime(2026, 5, 18),
    schedule=None,
    catchup=False,
    tags=["glue", "spark", "test"],
) as dag:

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