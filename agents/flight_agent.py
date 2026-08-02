from __future__ import annotations

import json
from datetime import date, timedelta
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from graph.state import TravelState

from tools.flight_tool import search_flights


def flight_agent(state:TravelState):
    query = state["user_query"]
    flight_data = search_flights(query)
