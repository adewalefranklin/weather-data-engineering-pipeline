from weather_pipeline.pipeline import WeatherPipeline
from weather_pipeline.logger import get_logger

logger = get_logger(__name__)


def main():
    pipeline = WeatherPipeline()
    locations = [
        {"city": "Cologne", "country": "Germany"},
        {"city": "Accra", "country": "Ghana"},
        {"city": "Lagos", "country": "Nigeria"},
    ]
    start_date = "2026-05-01"
    end_date = "2026-05-15"
    s3_keys = pipeline.run(locations, start_date, end_date, timeout=10)
    logger.info(f"Pipeline execution successfully completed! Data Stored at: {s3_keys}")


if __name__ == "__main__":
    main()
