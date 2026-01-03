from app.tools.db_tool import get_connection
from datetime import date

def meeting_exists(meeting_date: date, city: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "select 1 from meetings where meeting_date=%s and city=%s",
        (meeting_date, city)
    )

    exists = cur.fetchone() is not None
    cur.close()
    conn.close()
    return exists


def create_meeting(title: str, meeting_date: date, city: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "insert into meetings (title, meeting_date, city) values (%s, %s, %s)",
        (title, meeting_date, city)
    )

    conn.commit()
    cur.close()
    conn.close()
