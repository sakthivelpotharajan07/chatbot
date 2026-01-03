import requests
from datetime import datetime, timedelta, timezone, date
from app.config import OPENWEATHER_API_KEY

CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


def get_weather(city: str, day: str) -> str:
    if day == "today":
        return _today(city)
    elif day == "tomorrow":
        return _tomorrow(city)
    elif day == "yesterday":
        return (
            "Yesterday’s weather data is not available "
            "in the free OpenWeather API plan."
        )
    else:
        return "I could not understand the date."


def _today(city: str) -> str:
    res = requests.get(CURRENT_URL, params={
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }).json()

    if "main" not in res:
        return f"Weather error: {res.get('message', 'Unknown error')}"

    return (
        f"Today's weather in {city}: "
        f"{res['main']['temp']}°C, {res['weather'][0]['description']}."
    )


def _tomorrow(city: str) -> str:
    res = requests.get(FORECAST_URL, params={
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }).json()

    if "list" not in res:
        return f"Weather error: {res.get('message', 'Unknown error')}"

    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    for item in res["list"]:
        if datetime.fromtimestamp(item["dt"]).date() == tomorrow:
            return (
                f"Tomorrow's weather in {city}: "
                f"{item['main']['temp']}°C, "
                f"{item['weather'][0]['description']}."
            )

    return "Tomorrow's forecast is unavailable."


def get_weather_structured(city: str, target_date: date) -> dict:
    """
    Safe structured weather fetch for agent use.
    Never raises raw exceptions.
    """

    url = (
        "https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
    except Exception:
        return {
            "error": "Failed to connect to weather service"
        }

    # API-level error (city not found, etc.)
    if "list" not in data:
        return {
            "error": data.get("message", "Invalid weather data")
        }

    for item in data["list"]:
        forecast_date = item["dt_txt"].split(" ")[0]
        if forecast_date == target_date.isoformat():
            return {
                "description": item["weather"][0]["description"],
                "temperature": item["main"]["temp"]
            }

    return {
        "error": "No forecast available for the requested date"
    }