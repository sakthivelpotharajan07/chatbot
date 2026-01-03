import os
from app.tools.weather_tools import get_weather

USE_MOCK = os.getenv("USE_MOCK_WEATHER", "false").lower() == "true"

def get_weather_data(city: str, day: str) -> str:
    return get_weather(city, day)
