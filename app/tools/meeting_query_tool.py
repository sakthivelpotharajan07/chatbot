from datetime import date
from app.tools.db_tool import get_connection

def fetch_meetings(start_date: date, end_date: date):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT title, meeting_date, city
        FROM meetings
        WHERE meeting_date BETWEEN %s AND %s
        ORDER BY meeting_date
        """,
        (start_date, end_date)
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return rows
