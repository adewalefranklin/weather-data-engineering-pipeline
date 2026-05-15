from weather_pipeline.exceptions import LoadError
import boto3
import json
from datetime import datetime, timezone
from weather_pipeline.logger import get_logger


class S3Loader:
    def __init__(
        self, aws_access_key_id, aws_secret_access_key, aws_region, bucket_name, prefix
    ):
        self.logger = get_logger(self.__class__.__name__)
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region,
        )

    def s3_upload(self, data, location, start_date, end_date):
        self.logger.info("Initializing data upload on to s3 Bucket")
        try:
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            payload = {
                "data": data,
                "location": location,
                "start_date": start_date,
                "end_date": end_date,
                "ingestion_time": datetime.now(timezone.utc).isoformat(),
            }
            city = location["city"]
            country = location["country"]

            safe_location = f"{city}_{country}".replace(" ", "_")

            s3_key = f"{self.prefix}/{safe_location}/{start_date}.json"
            self.logger.info(f"Uploading data to S3 with key: {s3_key}")

            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=json.dumps(payload, default=str),
            )
            self.logger.info(f"Weather Data successfully Uploaded on to s3 Bucket")
            return s3_key
        except Exception as e:
            self.logger.error(f"Weather Data Upload Failed: {e}")
            raise LoadError(f"Weather data upload could not be completed: {e}") from e
