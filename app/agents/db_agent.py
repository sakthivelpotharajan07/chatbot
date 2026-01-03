from app.utils.db_intent_parser import parse_db_query_intent
from app.tools.meeting_query_tool import fetch_meetings

def handle_db_query(user_query: str) -> str:
    intent = parse_db_query_intent(user_query)

    meetings = fetch_meetings(
        start_date=intent["start"],
        end_date=intent["end"]
    )

    if not meetings:
        return "📭 No meetings found for the requested period."

    response = "📅 Meetings:\n"
    for title, meeting_date, city in meetings:
        response += f"- {title} on {meeting_date} at {city}\n"

    return response
