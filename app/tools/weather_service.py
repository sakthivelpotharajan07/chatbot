import requests
from datetime import date
from app.config import OPENWEATHER_API_KEY

def get_weather_structured(city: str, target_date: date) -> dict:
    """
    Calls OpenWeather API and returns structured weather data.
    NEVER raises exceptions.
    """

    url = (
        "https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
    except Exception:
        return {"error": "Failed to connect to weather service"}

    # API error (city not found, etc.)
    if "list" not in data:
        return {"error": data.get("message", "Invalid weather data")}

    # Match forecast date
    for item in data["list"]:
        if item["dt_txt"].startswith(target_date.isoformat()):
            return {
                "description": item["weather"][0]["description"],
                "temperature": item["main"]["temp"]
            }

    return {"error": "No forecast available for the requested date"}
