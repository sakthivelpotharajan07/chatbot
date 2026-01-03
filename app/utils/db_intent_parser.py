from datetime import date, timedelta

def parse_db_query_intent(user_query: str) -> dict:
    query = user_query.lower()

    today = date.today()

    if "today" in query:
        return {
            "start": today,
            "end": today
        }

    if "tomorrow" in query:
        tmr = today + timedelta(days=1)
        return {
            "start": tmr,
            "end": tmr
        }

    if "next week" in query:
        start = today + timedelta(days=1)
        end = today + timedelta(days=7)
        return {
            "start": start,
            "end": end
        }

    # Default → all upcoming
    return {
        "start": today,
        "end": today + timedelta(days=30)
    }
