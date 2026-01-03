import re
from datetime import date, timedelta

# Words that should never be part of a city name
STOP_WORDS = {
    "today", "tomorrow", "weather", "meeting", "schedule",
    "book", "create", "if", "is", "good", "check", "verify",
    "and", "to", "a", "the", "on", "for"
}

# Controlled vocabulary of supported cities
KNOWN_CITIES = {
    "chennai",
    "delhi",
    "mumbai",
    "bangalore",
    "bengaluru",
    "hyderabad",
    "kolkata",
    "pune",
    "kochi",
    "trivandrum"
}

def parse_meeting_intent(user_query: str) -> dict:
    query = user_query.lower()

    intent = None
    meeting_date = None
    city = None
    requires_good_weather = False

    # 1️⃣ Detect intent
    if any(word in query for word in ["schedule", "book", "create", "set up"]):
        intent = "schedule_meeting"

    # 2️⃣ Detect date
    if "tomorrow" in query:
        meeting_date = date.today() + timedelta(days=1)
    elif "today" in query:
        meeting_date = date.today()

    # 3️⃣ Detect weather condition
    if "weather is good" in query or "if the weather is good" in query:
        requires_good_weather = True

    # 4️⃣ City extraction — Case 1: "in <city>"
    city_match = re.search(r"in\s+([a-zA-Z\s]+)", query)
    if city_match:
        raw_city = city_match.group(1).strip()
        words = []

        for w in raw_city.split():
            if w in STOP_WORDS:
                continue
            if len(w) <= 2:      # 🔒 remove junk like "a", "to"
                continue
            words.append(w)

        if words:
            city = words[0].title()  # 🔒 take only the first valid token

    # 5️⃣ City extraction — Case 2: standalone city
    if not city:
        for known_city in KNOWN_CITIES:
            if known_city in query:
                city = known_city.title()
                break

    # 6️⃣ Fallback city (only if nothing found)
    if not city:
        city = "Chennai"

    return {
        "intent": intent,
        "meeting_date": meeting_date,
        "city": city,
        "requires_good_weather": requires_good_weather
    }
