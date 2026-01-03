import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# OpenWeather API Key
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not OPENWEATHER_API_KEY:
    raise RuntimeError(
        "OPENWEATHER_API_KEY is not set. "
        "Please add it to your .env file."
    )
