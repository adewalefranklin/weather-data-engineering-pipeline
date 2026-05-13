import os 
from dotenv import load_dotenv

load_dotenv()

class Config:
    required_vars=[
         # API
        "API_KEY",
        "BASE_URL",
    ]

    @classmethod
    def get(cls,key):
        value = os.getenv(key)
        if value is None:
            raise ValueError(f"{key} is not set in the environment variables.")
        return value
    @classmethod
    def validate(cls):
        for var in cls.required_vars:
            cls.get(var)