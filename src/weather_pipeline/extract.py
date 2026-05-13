from weather_pipeline.exceptions import ExtractError
import requests
from weather_pipeline.logger import get_logger


class WeatherExtract:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        self.logger = get_logger(self.__class__.__name__)

    def fetch_weather(self, location, start_date, end_date):
        self.logger.info("Initializing weather fetch")
        try:
            base_url = self.base_url.rstrip("/")

            url = (
                f"{base_url}/{location}/{start_date}/{end_date}"
                f"?unitGroup=metric&key={self.api_key}&contentType=json"
            )
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            self.logger.info(
                f"weather data for {location}, between {start_date} and {end_date} successfully fetched"
            )
            return data
        except Exception as e:
            self.logger.error(f"failed to fetch weather data: {e}")
            raise ExtractError(f"API call failed: {e}") from e
