# Weather and Energy Intelligence Platform

An end-to-end cloud-native data engineering platform that ingests weather and energy market data, processes it using Spark and Databricks, stores curated datasets in Snowflake, orchestrates workflows with Airflow, and visualizes insights in Power BI.


# Architecture

API
↓
AWS S3 Raw Layer
↓
Spark / Databricks
↓
Parquet / Delta
↓
Snowflake
↓
dbt
↓
Power BI