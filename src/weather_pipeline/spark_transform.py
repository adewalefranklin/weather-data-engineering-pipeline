from pyspark.sql import SparkSession
from weather_pipeline.config import Config
import pyspark.sql.functions as F


def create_spark_session():

    Config.validate()

    spark = (
        SparkSession.builder.appName("WeatherSparkTransformation")
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.4.1")
        .config("spark.hadoop.fs.s3a.access.key", Config.get("AWS_ACCESS_KEY_ID"))
        .config("spark.hadoop.fs.s3a.secret.key", Config.get("AWS_SECRET_ACCESS_KEY"))
        .config(
            "spark.hadoop.fs.s3a.aws.credentials.provider",
            "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
        )
        .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")

    return spark


if __name__ == "__main__":

    spark = create_spark_session()

    print("SparkSession created successfully")
    print(spark.version)

    raw_path = (
        "s3a://revised-weather-pipeline/raw/weather/Lagos_Nigeria/2026-05-01.json"
    )

    df = spark.read.option("multiline", "true").json(raw_path)

    daily_df = df.select(
        F.col("location.city").alias("city"),
        F.col("location.country").alias("country"),
        F.col("start_date"),
        F.col("end_date"),
        F.col("ingestion_time"),
        F.explode(F.col("data.days")).alias("day"),
    )

flattened_daily_df = daily_df.select(
    F.col("city"),
    F.col("country"),
    F.col("day.datetime").alias("weather_date"),
    F.col("day.temp").alias("avg_temp"),
    F.col("day.tempmax").alias("max_temp"),
    F.col("day.tempmin").alias("min_temp"),
    F.col("day.humidity"),
    F.col("day.conditions"),
    F.col("day.precip"),
    F.col("day.windspeed"),
)

weekly_avg_temp_df = flattened_daily_df.groupBy("city", "country").agg(
    F.round(F.avg("avg_temp"), 2).alias("avg_city_temp")
)

weekly_avg_temp_df.printSchema()
weekly_avg_temp_df.show()

output_path = "data/transformed/weather/daily"

flattened_daily_df.write.mode("overwrite").parquet(output_path)

# flattened_daily_df.write \
#     .format("delta") \
#     .mode("overwrite") \
#     .save(output_path)

spark.stop()
