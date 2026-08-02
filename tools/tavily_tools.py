from __future__ import annotations
import os
from typing import Any
from langchain_core.tools import tool
from tavily import TavilyClient


def _client() -> TavilyClient:##api checking
    key = os.getenv("TAVILY_API_KEY")
    if not key:
        raise RuntimeError("TAVILY_API_KEY is not set in the environment")
    return TavilyClient(api_key=key)


@tool
def search_hotels(
    destination: str,
    check_in: str,
    check_out: str,
    adults: int = 1,
) -> dict[str, Any]:
    """Search the web for hotels in a destination for given check-in/check-out dates.

    `destination` is a city name (not an airport code).
    `check_in` and `check_out` are YYYY-MM-DD.
    Returns {destination, check_in, check_out, adults, answer, results[]}.
    """
    query = (
        f"best hotels in {destination} for {adults} adult(s) "
        f"from {check_in} to {check_out}, including price per night and location"
    )
    try:
        response = _client().search(
            query=query,
            max_results=5,
            api_key=os.getenv("TAVILY_API_KEY")
        )
    except Exception as exc:
        return {"error": f"tavily request failed: {exc}", "results": []}

    return {
        "destination": destination,
        "check_in": check_in,
        "check_out": check_out,
        "adults": adults,
        "answer": response.get("answer"),
        "results": [
            {"title": r.get("title"), "url": r.get("url"), "content": r.get("content")}
            for r in response.get("results", [])
        ],
    }
