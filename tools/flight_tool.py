from __future__ import annotations

import os
from typing import Any
from dotenv import load_dotenv
import requests
from langchain_core.tools import tool

load_dotenv()

AVIATIONSTACK_BASE = "https://api.aviationstack.com/v1"


def _require_key() -> str:
    key = os.getenv("AVIATION_API_KEY") or os.getenv("API_KEY")
    if not key:
        raise RuntimeError("AVIATION_API_KEY or API_KEY is not set in the environment")
    return key

@tool
def search_flights(query: str) -> dict[str, Any]:
    """Search the web for flights matching a query.
    `query` is a string describing the flight search.
    Returns {query, answer, results[]}.
    """
    key = _require_key()
    url = f"{AVIATIONSTACK_BASE}/flights"
    params = {"access_key": key, "search": query, "limit": 5}

    try:
        response = requests.get(url, params=params)
        data = response.json()
    except Exception as exc:
        return {"error": f"aviationstack request failed: {exc}", "results": []}


    flights=[]

    if "data" in data:
        for flight in data["data"][:5]:
            airplane = flight.get("airline", {}).get("name","Unknown")
            departure = flight.get("departure", {}).get("airport")
            arrival = flight.get("arrival", {}).get("airport")
            status = flight.get("flight_status", {}).get("name")

            flights.append({
                "airplane": airplane,
                "departure": departure,
                "arrival": arrival,
                "status": status,
            })

    return {
    "query": query,
    "answer": f"Found {len(flights)} flights.",
    "results": flights,
}