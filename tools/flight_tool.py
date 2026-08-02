from __future__ import annotations

import os
from typing import Any
from dotenv import load_dotenv
import json
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


    flights = []

    flights_data = data.get("data", []) if isinstance(data, dict) else []

    for raw in flights_data[:5]:
        try:
            # Normalize flight entry to a dict. Some APIs may return JSON strings or unexpected types.
            if isinstance(raw, str):
                try:
                    flight = json.loads(raw)
                except Exception:
                    # couldn't parse string -> skip
                    continue
            elif isinstance(raw, dict):
                flight = raw
            else:
                # unknown type, skip
                continue

            # airline name
            airline = flight.get("airline")
            if isinstance(airline, dict):
                airplane = airline.get("name", "Unknown")
            elif isinstance(airline, str):
                airplane = airline
            else:
                airplane = "Unknown"

            # departure / arrival airports
            dep = flight.get("departure")
            if isinstance(dep, dict):
                departure = dep.get("airport") or dep.get("iata") or None
            else:
                departure = dep

            arr = flight.get("arrival")
            if isinstance(arr, dict):
                arrival = arr.get("airport") or arr.get("iata") or None
            else:
                arrival = arr

            # status may be a dict or string
            status_val = flight.get("flight_status") or flight.get("status")
            if isinstance(status_val, dict):
                status = status_val.get("name") or status_val.get("status") or str(status_val)
            else:
                status = status_val

            flights.append({
                "airplane": airplane,
                "departure": departure,
                "arrival": arrival,
                "status": status,
            })
        except Exception:
            # be tolerant of malformed entries
            continue

    return {
    "query": query,
    "answer": f"Found {len(flights)} flights.",
    "results": flights,
}