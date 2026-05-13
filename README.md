# Weather and Energy Intelligence Platform

An end-to-end cloud-native data engineering platform that ingests weather and energy market data, processes it using Spark and Databricks, stores curated datasets in Snowflake, orchestrates workflows with Airflow, and visualizes insights in Power BI.


# Architecture

API
↓
S3 raw
↓
Spark/Databricks
↓
S3 transformed
↓
Snowflake
↓
dbt
↓
Power BI