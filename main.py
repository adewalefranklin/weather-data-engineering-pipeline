from weather_pipeline.pipeline import WeatherPipeline
from weather_pipeline.logger import get_logger

logger = get_logger(__name__)


def main():
    pipeline = WeatherPipeline()
    locations = [
        {"city": "Lagos", "country": "Nigeria"},
        {"city": "London", "country": "United Kingdom"},
        {"city": "Nairobi", "country": "Kenya"},
        {"city": "New Dehli", "country": "India"}
        {"city": "Port Louis", "country": "Mauritius"}
        {"city": "Cologne", "country": "Germany"}
        {"city": "Dubai", "country": "United Arab Emirates"},
        {"city": "Arizona", "country": "United States of America"},
        {"city": "Shanghai", "country": "China"},
        {"city": "Kingston", "country": "Jamaica"}
    ]
    start_date = "2026-05-01"
    end_date = "2026-05-05"
    s3_keys = pipeline.run(locations, start_date, end_date)
    logger.info(f"Pipeline execution successfully completed! Data Stored at: {s3_keys}")


if __name__ == "__main__":
    main()
