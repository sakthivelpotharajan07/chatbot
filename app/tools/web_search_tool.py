from duckduckgo_search import DDGS

def web_search(query: str) -> str:
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=3))

    if not results:
        return "No relevant web results found."

    return results[0]["body"]
