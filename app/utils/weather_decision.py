def is_good_weather(weather_data: dict) -> bool:
    """
    Decide if weather is suitable for meeting.
    """

    condition = weather_data["description"].lower()
    temp = weather_data["temperature"]

    if "rain" in condition or "storm" in condition:
        return False

    if temp < 18 or temp > 35:
        return False

    return True
