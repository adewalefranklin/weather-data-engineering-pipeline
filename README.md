# Weather and Energy Intelligence Platform

An end-to-end cloud-native data engineering platform that ingests weather and energy market data, processes it using Spark and Databricks, stores curated datasets in Snowflake, orchestrates workflows with Airflow, and visualizes insights in Power BI.


# Architecture

Weather API
↓
Python ingestion
↓
S3 raw JSON
↓
Glue Spark ETL
↓
Partitioned parquet
↓
Glue Crawler
↓
Glue Data Catalog
↓
Athena SQL query