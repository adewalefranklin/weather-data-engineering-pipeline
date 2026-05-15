import pytest
import requests
from weather_pipeline.extract import WeatherExtractor


def test_extract_success(mocker):
    fake_response = mocker.Mock()
    fake_response.raise_for_status.return_value = None
    fake_response.json.return_value = {"temp": 20}
    mock_get = mocker.patch(
        "weather_pipeline.extract.requests.get", return_value=fake_response
    )
    extractor = WeatherExtractor("fake_api", "fake_base_url")
    result = extractor.fetch_weather("Berlin", "2026-05-01", "2026-05-15")
    assert result == {"temp": 20}
    mock_get.assert_called_once
