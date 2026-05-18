from weather_pipeline.extract import WeatherExtractor
from weather_pipeline.load import S3Loader
from weather_pipeline.logger import get_logger
from weather_pipeline.exceptions import PipelineError
from weather_pipeline.config import Config
import time


class WeatherPipeline:
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        Config.validate()

    def run(self, locations, start_date, end_date):
        try:
            s3_keys = []
            self.extractor = WeatherExtractor(
                api_key=Config.get("API_KEY"), base_url=Config.get("BASE_URL")
            )
            self.loader = S3Loader(
                aws_access_key_id=Config.get("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=Config.get("AWS_SECRET_ACCESS_KEY"),
                aws_region=Config.get("AWS_REGION"),
                bucket_name=Config.get("AWS_S3_BUCKET_NAME"),
                prefix=Config.get("AWS_RAW_PREFIX"),
            )
            for location in locations:
                city = location["city"]
                country = location["country"]
                location_query = f"{city},{country}"

                self.logger.info(
                    f"Starting pipeline for {location_query} from {start_date} to {end_date}"
                )

                data = self.extractor.fetch_weather(
                    location_query, start_date, end_date
                )
                s3_key = self.loader.s3_upload(data, location, start_date, end_date)
                s3_keys.append(s3_key)
                self.logger.info(
                    f"Successfully uploaded weather data for {location_query} to S3"
                )
                self.logger.info("Successfully uploaded all location data to S3")
            return s3_keys

        except Exception as e:
            self.logger.error("Pipeline failed")
            raise PipelineError(f"Pipeline execution failed: {e}") from e
