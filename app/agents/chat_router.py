from app.agents.meeting_agent import handle_meeting_query
from app.agents.db_agent import handle_db_query
from app.agents.document_agent import handle_document_query
from app.agents.weather_agent import get_weather_for_date
from datetime import date

def route_query(user_query: str) -> dict:
    q = user_query.lower()

    # 1️⃣ Meeting scheduling
    if any(word in q for word in ["schedule", "book", "set up"]):
        return {
            "agent": "meeting",
            "response": handle_meeting_query(user_query)
        }

    # 2️⃣ Meeting database queries
    if "meeting" in q and any(word in q for word in ["show", "list", "do we have"]):
        return {
            "agent": "database",
            "response": handle_db_query(user_query)
        }

    # 3️⃣ Document questions
    if any(word in q for word in ["document", "policy", "resume", "cv", "file", "summarize", "explained", "content", "report", "what does it say"]):
        return {
            "agent": "document",
            "response": handle_document_query(user_question=user_query)
        }

    # 4️⃣ Weather queries
    if "weather" in q:
        from app.agents.weather_agent import handle_weather_query
        return {
            "agent": "weather",
            "response": handle_weather_query(user_query)
        }

    # 5️⃣ Fallback
    return {
        "agent": "unknown",
        "response": "❌ I couldn't determine which agent should handle this request."
    }
