import re

STOP_WORDS = ["today", "tomorrow", "yesterday"]

def extract_city(text: str) -> str:
    text = text.lower()

    # Look for "in <city>"
    match = re.search(r"in\s+([a-zA-Z\s]+)", text)
    if not match:
        return "Chennai"

    city_part = match.group(1)

    # Remove stop words
    for word in STOP_WORDS:
        city_part = city_part.replace(word, "")

    # Remove trailing punctuation
    city_part = re.sub(r"[^\w\s]", "", city_part)

    return city_part.strip().title()
