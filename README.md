# Weather Intelligence Platform

This project is an end-to-end cloud-native data engineering pipeline that extracts weather data from the Visual Crossing API, stores raw data in AWS S3, performs Spark-based transformations using AWS Glue, orchestrates workflows with Apache Airflow, and prepares transformed data for analytics and reporting.


# Architecture

                ┌──────────────────────┐
                │  Developer / VS Code │
                └──────────┬───────────┘
                           │
                           │ Git Commit / Push
                           ▼
                ┌──────────────────────┐
                │   GitHub Repository  │
                └──────────┬───────────┘
                           │
                           │ CI/CD Trigger
                           ▼
                ┌──────────────────────┐
                │ GitHub Actions CI/CD │
                │ pytest + Docker Build│
                └──────────┬───────────┘
                           │
                           │ Validated Code
                           ▼
                ┌──────────────────────┐
                │ Dockerized Pipeline  │
                │ Python Runtime Image │
                └──────────┬───────────┘
                           │
                           │ Runs Extract App
                           ▼
                ┌──────────────────────┐
                │  Visual Crossing API │
                └──────────┬───────────┘
                           │
                           │ REST API Request
                           ▼
                ┌──────────────────────┐
                │ Python Extract Layer │
                │  (WeatherExtractor)  │
                └──────────┬───────────┘
                           │
                           │ Raw JSON Payload
                           ▼
                ┌──────────────────────┐
                │ AWS S3 Raw Storage   │
                │ raw/weather/...json  │
                └──────────┬───────────┘
                           │
                           │ Triggered by Airflow
                           ▼
                ┌──────────────────────┐
                │ Apache Airflow DAG   │
                │ retries + scheduling │
                └──────────┬───────────┘
                           │
                           │ GlueJobOperator
                           ▼
                ┌──────────────────────┐
                │ AWS Glue ETL Job     │
                │ Managed Spark Engine │
                └──────────┬───────────┘
                           │
                           │ Reads Spark Script
                           ▼
      ┌────────────────────────────────────────┐
      │ Glue Spark Script stored in AWS S3     │
      │ Weather ETL Spark Transformation.py    │
      └────────────────┬───────────────────────┘
                       │
                       │ Spark Transformations
                       ▼
            ┌─────────────────────────┐
            │ PySpark Transformation  │
            │ Flatten + Clean Data    │
            └──────────┬──────────────┘
                       │
                       │ Parquet Output
                       ▼
            ┌─────────────────────────┐
            │ AWS S3 Transformed Zone │
            │ transformed/weather/    │
            └──────────┬──────────────┘
                       │
                       │ Analytics Layer
                       ▼
            ┌─────────────────────────┐
            │ Snowflake / Athena / BI │
            │ Power BI Consumption    │
            └─────────────────────────┘

# Project Components

1. Extraction Layer (Python)
Responsibilities
Connects to Visual Crossing Weather API
Fetches weather data dynamically
Handles API requests and errors
Packages raw JSON payloads

## Main Modules

extract.py
pipeline.py
config.py
exceptions.py
logger.py

### Technologies

Python
requests
boto3
dotenv
logging

2. Raw Data Storage Layer

AWS S3 Raw Zone

Stores unprocessed API responses as JSON files.

Example:

s3://revised-weather-pipeline/raw/weather/Cologne_Germany/2026-05-01.json

### Purpose

Raw immutable storage
Replay capability
Auditability
Decouples extraction from transformation

3. Orchestration Layer
Apache Airflow

## Airflow orchestrates the entire workflow.

Responsibilities
Schedule pipelines
Trigger extraction
Trigger AWS Glue jobs
Monitor pipeline execution
Retry failed tasks
Centralized logging

### DAGs

weather_dag.py
extract_dag.py
transform_dag_test.py

### Operators Used

PythonOperator
GlueJobOperator

4. Transformation Layer

## AWS Glue + Spark

Glue provides managed Spark infrastructure for scalable transformations.

Responsibilities
Read raw JSON from S3
Flatten nested weather data
Transform into analytics-friendly schema
Write parquet outputs


## Spark Script

Weather ETL Spark Transformation.py

## Spark Operations

JSON ingestion
DataFrame transformations
Column flattening
Parquet output writing

### Technologies

PySpark
AWS Glue
Spark DataFrames

5. Transformed Data Zone
AWS S3 Processed Layer

Stores cleaned parquet files.

Example:

s3://revised-weather-pipeline/transformed/weather/

### Benefits:

Columnar storage
Faster analytics queries
Optimized for BI tools
Partition-ready architecture

6. Analytics & Consumption Layer

## Potential consumers:

Snowflake
AWS Athena
Power BI
dbt models
Databricks
Machine learning pipelines

## Security Architecture

IAM Users:

airflow-orchestration-user

Used by Airflow to:

Trigger Glue jobs
Access S3
Read IAM roles

## IAM Roles

AWSGlueServiceRole-practice

Used by AWS Glue itself to:

Execute Spark jobs
Access S3 buckets
Write logs
Manage Glue execution

## Authentication & Authorization Flow

Airflow
↓
AWS Access Keys
↓
IAM User Authentication
↓
IAM Policy Authorization
↓
Glue Job Trigger
↓
Glue Role Assumption
↓
Spark Execution

## Key Cloud Engineering Concepts Implemented

Data Engineering
ETL/ELT pipelines
Raw vs transformed zones
Distributed processing
Pipeline orchestration

## Cloud Engineering

IAM users and roles
Least privilege access
S3 architecture
Glue managed Spark

## Orchestration

DAG design
Task dependencies
Retry handling
Workflow automatio

## Tech Stack

| Layer               | Technology                  |
| ------------------- | --------------------------- |
| Extraction          | Python                      |
| API                 | Visual Crossing Weather API |
| Storage             | AWS S3                      |
| Orchestration       | Apache Airflow              |
| Transformation      | AWS Glue                    |
| Distributed Compute | Apache Spark                |
| Data Format         | JSON / Parquet              |
| Cloud               | AWS                         |
| Analytics           | Snowflake / Power BI        |
| Version Control     | Git/GitHub                  |
| Containerization    | Docker                      |


## Future Improvements

Snowpipe ingestion into Snowflake
dbt transformation layer
CI/CD with GitHub Actions
Airflow deployment on MWAA
Terraform infrastructure automation
Data quality checks
Monitoring & alerting
Incremental processing
Partition optimization
Lakehouse architecture evolution

