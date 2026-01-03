from datetime import date, timedelta

from app.utils.meeting_intent_parser import parse_meeting_intent
from app.agents.weather_agent import get_weather_for_date
from app.utils.weather_decision import is_good_weather
from app.tools.meeting_tool import meeting_exists, create_meeting


def handle_meeting_query(user_query: str) -> str:
    """
    Agent 3: Weather + Meeting Scheduling Agent
    """

    # 1️⃣ Parse intent
    intent_data = parse_meeting_intent(user_query)

    if intent_data["intent"] != "schedule_meeting":
        return "❌ Unable to understand meeting request."

    meeting_date = intent_data["meeting_date"] or (date.today() + timedelta(days=1))
    city = intent_data["city"]

    # 2️⃣ Weather check (Agent 1)
    weather = get_weather_for_date(city, meeting_date)

    # Handle weather failure
    if not isinstance(weather, dict) or "error" in weather:
        reason = weather.get("error", "Unknown weather error")
        return (
            f"❌ Unable to verify weather for {city} on {meeting_date}.\n"
            f"Reason: {reason}."
        )

    # 3️⃣ Weather reasoning
    if intent_data["requires_good_weather"]:
        if not is_good_weather(weather):
            return (
                f"❌ Meeting not scheduled.\n"
                f"Reason: Bad weather expected in {city} on {meeting_date} "
                f"({weather['description']}, {weather['temperature']}°C)."
            )

    # 4️⃣ DB check
    if meeting_exists(meeting_date, city):
        return (
            f"ℹ️ Meeting already exists on {meeting_date} in {city}.\n"
            f"Weather: {weather['description']}, {weather['temperature']}°C."
        )

    # 5️⃣ Create meeting
    create_meeting(
        title="Team Meeting",
        meeting_date=meeting_date,
        city=city
    )

    return (
        f"✅ Meeting scheduled successfully.\n"
        f"Date: {meeting_date}\n"
        f"City: {city}\n"
        f"Weather: {weather['description']}, {weather['temperature']}°C."
    )
