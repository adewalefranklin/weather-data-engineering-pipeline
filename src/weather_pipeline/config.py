import os
from dotenv import load_dotenv
from weather_pipeline.exceptions import ConfigError

load_dotenv()


class Config:
    required_vars = [
        # API
        "API_KEY",
        "BASE_URL",
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_REGION",
        "AWS_S3_BUCKET_NAME",
        "AWS_RAW_PREFIX",
        "AWS_TRANSFORMED_PREFIX",
    ]

    @classmethod
    def get(cls, key):
        value = os.getenv(key)
        if value is None:
            raise ConfigError(f"{key} is not set in the environment variables.")
        return value

    @classmethod
    def validate(cls):
        for var in cls.required_vars:
            cls.get(var)
