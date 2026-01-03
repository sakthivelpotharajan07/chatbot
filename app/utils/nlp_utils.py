def extract_day(text: str) -> str:
    text = text.lower()

    if "tomorrow" in text:
        return "tomorrow"
    if "yesterday" in text:
        return "yesterday"
    return "today"
